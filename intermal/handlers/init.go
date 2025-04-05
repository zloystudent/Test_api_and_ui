package handlers

import (
	"context"
	"fmt"
	"net/http"
	"server-test/intermal/dto"
	"server-test/intermal/entity"
	"server-test/intermal/storage"
	"strconv"
	"time"

	"github.com/gofiber/fiber/v2"
	"github.com/sirupsen/logrus"
)

type HandlerSetup struct {
	Storage storage.Storage
	Logger  *logrus.Logger
}

type Handler struct {
	storage storage.Storage
	logger  *logrus.Logger
}

func NewHandler(setup HandlerSetup) *Handler {
	return &Handler{
		storage: setup.Storage,
		logger:  setup.Logger,
	}
}

func (h *Handler) Use(r fiber.Router) {
	r.Get("/time", func(c *fiber.Ctx) error {
		return c.SendString(time.Now().String())
	})

	r.Post("/create", h.Create)
	r.Get("/get/:id", h.Get)
	r.Delete("/delete/:id", h.Delete)
	r.Post("/getAll", h.GetAll)
	r.Get("/getAll", h.GetAllQuery)
	r.Patch("/patch/:id", h.UpdateEntity)

}

// @Summary      Список сущностей
// @Description  Запрос на получение списка сущностей
// @Accept       x-www-form-urlencoded
// @Produce      json
// @Tags         Entity
// @Param        title     query    string   false   "Заголовок"
// @Param        verified  query    bool     false   "Подтверждено"
// @Param        page      query    int      false   "Страница"
// @Param        perPage   query    int      false   "Элементов на странице"
// @Success      200 {object} []dto.EntityResponse
// @Failure      400
// @Failure      500
// @Router       /api/getAll [get]
func (h *Handler) GetAllQuery(c *fiber.Ctx) error {
	title := c.Query("title")
	verified := c.Query("verified")
	page := c.Query("page")
	perPage := c.Query("perPage")

	filter := entity.EntityFilter{}

	if title != "" {
		filter.Title = &title
	}

	if verified != "" {
		v, err := strconv.ParseBool(verified)
		if err != nil {
			return c.Status(http.StatusBadRequest).JSON(map[string]interface{}{
				"error": err.Error(),
			})
		}

		filter.Verified = &v
	}

	if page != "" {
		p64, err := strconv.ParseUint(page, 10, 0)
		if err != nil {
			return c.Status(http.StatusBadRequest).JSON(map[string]interface{}{
				"error": err.Error(),
			})
		}

		p := uint(p64)

		filter.Page = &p
	}

	if perPage != "" {
		p64, err := strconv.ParseUint(perPage, 10, 0)
		if err != nil {
			return c.Status(http.StatusBadRequest).JSON(map[string]interface{}{
				"error": err.Error(),
			})
		}

		p := uint(p64)

		filter.PerPage = &p
	}

	ent, err := h.storage.GetAll(c.Context(), filter)
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(map[string]interface{}{
			"error": err.Error(),
		})
	}

	result := make([]dto.EntityResponse, 0, len(ent))

	for i := range ent {
		res := dto.EntityResponse{
			ID:               ent[i].ID,
			Title:            ent[i].Title,
			ImportantNumbers: ent[i].ImportantNumbers,
			Verified:         ent[i].Verified,
		}

		if ent[i].Addition.ID != nil {
			res.Addition = &dto.AdditionResponse{
				ID:               ent[i].Addition.ID,
				AdditionalInfo:   ent[i].Addition.AdditionalInfo,
				AdditionalNumber: ent[i].Addition.AdditionalNumber,
			}
		}

		result = append(result, res)
	}

	return c.JSON(dto.EntityFilterResponse{
		Entity:  result,
		Page:    filter.Page,
		PerPage: filter.PerPage,
	})
}

// @Summary      Обновление сущности и ее дополнений
// @Description  Отправка событий
// @Accept       json
// @Produce      plain
// @Tags         Entity
// @Param        id       path    string            true  "ID сущности"
// @Param        message  body    dto.EntityRequest  true  "Сущность"
// @Success      204
// @Failure      400
// @Failure      500
// @Router       /api/patch/{id} [patch]
func (h *Handler) UpdateEntity(c *fiber.Ctx) error {
	id, err := c.ParamsInt("id", 0)
	if err != nil || id <= 0 {
		return c.Status(http.StatusBadRequest).JSON(map[string]interface{}{
			"error": "the number of entities or the number of pages cannot be negative",
		})
	}

	check, err := h.storage.CheckEntityByID(c.Context(), id)
	if err != nil {
		return c.Status(http.StatusBadRequest).JSON(map[string]interface{}{
			"error": fmt.Sprintf("unable to check for existence of such id [%v]", err.Error()),
		})
	}

	req := new(dto.EntityRequest)

	if err := c.BodyParser(req); err != nil {
		return c.Status(http.StatusBadRequest).JSON(map[string]interface{}{
			"error": err.Error(),
		})
	}

	en := &entity.Entity{
		Title:            req.Title,
		Verified:         req.Verified,
		ImportantNumbers: req.ImportantNumbers,
	}

	var ad *entity.Addition

	if req.Addition != nil {
		ad = &entity.Addition{
			AdditionalInfo:   req.Addition.AdditionalInfo,
			AdditionalNumber: req.Addition.AdditionalNumber,
		}
	}

	if err := h.storage.ChangeEntity(c.Context(), id, *check.AdditionID, en, ad); err != nil {
		return c.Status(http.StatusInternalServerError).JSON(map[string]interface{}{
			"error": err.Error(),
		})
	}

	return c.SendStatus(http.StatusNoContent)
}

// // @Summary      Список сущностей
// // @Description  Запрос на получение списка сущностей
// // @Accept       json
// // @Produce      json
// // @Tags         Entity
// // @Param        message  body    dto.EntityFilterRequest  true  "Сущность (пустое тело допустимо)"
// // @Success      200 {object} []dto.EntityResponse
// // @Failure      400
// // @Failure      500
// // @Router       /api/getAll [post]
func (h *Handler) GetAll(c *fiber.Ctx) error {
	req := new(dto.EntityFilterRequest)

	if len(c.Body()) > 0 {
		if err := c.BodyParser(req); err != nil {
			return c.Status(http.StatusBadRequest).JSON(map[string]interface{}{
				"error": err.Error(),
			})
		}
	}

	filter := entity.EntityFilter{
		Title:    req.Title,
		Verified: req.Verified,
		Page:     req.Page,
		PerPage:  req.PerPage,
	}

	ent, err := h.storage.GetAll(c.Context(), filter)
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(map[string]interface{}{
			"error": err.Error(),
		})
	}

	result := make([]dto.EntityResponse, 0, len(ent))

	for i := range ent {
		res := dto.EntityResponse{
			ID:               ent[i].ID,
			Title:            ent[i].Title,
			ImportantNumbers: ent[i].ImportantNumbers,
			Verified:         ent[i].Verified,
		}

		if ent[i].Addition.ID != nil {
			res.Addition = &dto.AdditionResponse{
				ID:               ent[i].Addition.ID,
				AdditionalInfo:   ent[i].Addition.AdditionalInfo,
				AdditionalNumber: ent[i].Addition.AdditionalNumber,
			}
		}

		result = append(result, res)
	}

	return c.JSON(dto.EntityFilterResponse{
		Entity:  result,
		Page:    req.Page,
		PerPage: req.PerPage,
	})
}

// @Summary      Создание сущности
// @Description  Запрос на добавление новой сущности
// @Accept       json
// @Produce      plain
// @Tags         Entity
// @Param        message  body    dto.EntityRequest  true  "Сущность"
// @Success      200  string  "Номер созданной сущности"
// @Failure      400
// @Failure      500
// @Router       /api/create [post]
func (h *Handler) Create(c *fiber.Ctx) error {
	req := new(dto.EntityRequest)

	if err := c.BodyParser(req); err != nil {
		return c.Status(http.StatusBadRequest).JSON(map[string]interface{}{
			"error": err.Error(),
		})
	}

	en := &entity.Entity{
		Title:            new(string),
		Verified:         new(bool),
		ImportantNumbers: []int{},
	}

	var add *entity.Addition

	// add := &entity.Addition{
	// 	AdditionalInfo:   new(string),
	// 	AdditionalNumber: new(int),
	// }

	if req.Title == nil {
		return c.Status(http.StatusInternalServerError).JSON(map[string]interface{}{
			"error": "title field is required",
		})
	}

	en.Title = req.Title

	if req.Verified == nil {
		return c.Status(http.StatusInternalServerError).JSON(map[string]interface{}{
			"error": "verified field is required",
		})
	}

	en.Verified = req.Verified

	if req.ImportantNumbers != nil {
		en.ImportantNumbers = req.ImportantNumbers
	}

	if req.Addition != nil {
		add = &entity.Addition{}

		if req.Addition.AdditionalInfo != nil {
			add.AdditionalInfo = req.Addition.AdditionalInfo
		}

		if req.Addition.AdditionalNumber != nil {
			add.AdditionalNumber = req.Addition.AdditionalNumber
		}
	}

	id, err := h.storage.Create(context.Background(), en, add)
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(map[string]interface{}{
			"error": err.Error(),
		})
	}

	return c.SendString(strconv.Itoa(id))
}

// @Summary      Получить сущность
// @Description  Запрос на получение одной сущности
// @Produce      json
// @Tags         Entity
// @Param        id       path    string     true  "ID сущности"
// @Success      200 {object} dto.EntityResponse
// @Failure      400
// @Failure      500
// @Router       /api/get/{id} [get]
func (h *Handler) Get(c *fiber.Ctx) error {
	id, err := c.ParamsInt("id", 0)
	if err != nil {
		return c.Status(http.StatusBadRequest).JSON(map[string]interface{}{
			"error": err.Error(),
		})
	}

	ent, err := h.storage.GetEntityByID(c.Context(), id)
	if err != nil {
		return c.Status(http.StatusInternalServerError).JSON(map[string]interface{}{
			"error": err.Error(),
		})
	}

	result := dto.EntityResponse{
		ID:               ent.ID,
		Title:            ent.Title,
		Verified:         ent.Verified,
		ImportantNumbers: ent.ImportantNumbers,
	}

	if ent.Addition.ID != nil {
		result.Addition = &dto.AdditionResponse{
			ID:               ent.Addition.ID,
			AdditionalInfo:   ent.Addition.AdditionalInfo,
			AdditionalNumber: ent.Addition.AdditionalNumber,
		}
	}

	return c.JSON(result)
}

// @Summary      Удаление сущности
// @Description  Запрос на удаление сущности и ее дополнений
// @Produce      plain
// @Tags         Entity
// @Param        id       path    string            true  "ID сущности"
// @Success      204
// @Failure      400
// @Failure      500
// @Router       /api/delete/{id} [delete]
func (h *Handler) Delete(c *fiber.Ctx) error {
	id, err := c.ParamsInt("id", 0)
	if err != nil {
		return c.Status(http.StatusBadRequest).JSON(map[string]interface{}{
			"error": err.Error(),
		})
	}

	if err := h.storage.DeleteEntityByID(c.Context(), id); err != nil {
		return c.Status(http.StatusInternalServerError).JSON(map[string]interface{}{
			"error": err.Error(),
		})
	}

	return c.SendStatus(http.StatusNoContent)
}
