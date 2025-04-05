package dto

// EntityRequest model info.
// @Description Модель для отправки сущности.
type EntityRequest struct {
	// Title заголовок сущности.
	Title *string `json:"title" example:"Заголовок сущности"`
	// Verified статус верификации сущности.
	Verified *bool `json:"verified" example:"true"`
	// Addition дополнительная информация о событии.
	Addition *AdditionRequest `json:"addition"`
	// ImportantNumbers массив важных чисел для сущности.
	ImportantNumbers []int `json:"important_numbers" example:"42,87,15"`
}

// AdditionRequest model info.
// @Description Дополнительная информация о сущности.
type AdditionRequest struct {
	// AdditionalInfo дополнительные сведения о сущности.
	AdditionalInfo *string `json:"additional_info" example:"Дополнительные сведения"`
	// AdditionalNumber дополнительное число для сущности.
	AdditionalNumber *int `json:"additional_number" example:"123"`
}

// EntityFilterRequest model info.
// @Description Фильтр и пагинация для сущностей.
type EntityFilterRequest struct {
	// Title фильтрует сущности по заголовку.
	Title *string `json:"title" example:"Заголовок сущности"`
	// Verified фильтрует сущности по статусу верификации.
	Verified *bool `json:"verified" example:"true"`
	// Page указывает номер страницы для пагинации.
	Page *uint `json:"page" example:"1"`
	// PerPage определяет количество сущностей на странице.
	PerPage *uint `json:"perPage" example:"10"`
}

// EntityResponse информация о сущности в ответе.
type EntityResponse struct {
	// ID идентификатор сущности.
	ID int `json:"id" example:"1"`
	// Title заголовок сущности.
	Title string `json:"title" example:"Заголовок сущности"`
	// Verified статус верификации сущности.
	Verified bool `json:"verified" example:"true"`
	// Addition дополнительная информация о сущности.
	Addition *AdditionResponse `json:"addition,omitempty"`
	// ImportantNumbers массив важных чисел для сущности.
	ImportantNumbers []int `json:"important_numbers,omitempty" example:"42,87,15"`
}

// AdditionRequest model info.
// @Description Дополнительная информация о сущности.
type AdditionResponse struct {
	// ID идентификатор дополнительной информации.
	ID *int `json:"id" example:"1"`
	// AdditionalInfo дополнительные сведения о сущности.
	AdditionalInfo *string `json:"additional_info,omitempty" example:"Дополнительные сведения"`
	// AdditionalNumber дополнительное число для сущности.
	AdditionalNumber *int `json:"additional_number,omitempty" example:"123"`
}

type EntityFilterResponse struct {
	Entity  []EntityResponse `json:"entity"`
	Page    *uint            `json:"page,omitempty"`
	PerPage *uint            `json:"perPage,omitempty"`
}
