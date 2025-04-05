package storage

import (
	"context"
	"fmt"
	"server-test/intermal/entity"
	"strings"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"
)

type Storage interface {
	Create(context.Context, *entity.Entity, *entity.Addition) (int, error)
	GetAll(ctx context.Context, filter entity.EntityFilter) ([]entity.EntityAddition, error)
	CreateTX(ctx context.Context) (pgx.Tx, error)
	GetEntityByID(ctx context.Context, id int) (*entity.EntityAddition, error)
	DeleteEntityByID(ctx context.Context, id int) error
	CheckEntityByID(ctx context.Context, id int) (*entity.Entity, error)
	ChangeEntity(ctx context.Context, id int, additionID int, ent *entity.Entity, ad *entity.Addition) error
}

type storage struct {
	conn *pgxpool.Pool
}

type StorageSetup struct {
	Conn *pgxpool.Pool
}

func NewStorage(setup *StorageSetup) Storage {
	return &storage{
		conn: setup.Conn,
	}
}

func (s *storage) CreateTX(ctx context.Context) (pgx.Tx, error) {
	return s.conn.BeginTx(ctx, pgx.TxOptions{IsoLevel: pgx.ReadCommitted})
}

func (s *storage) CheckEntityByID(ctx context.Context, id int) (*entity.Entity, error) {
	result := new(entity.Entity)

	query := `SELECT 	
					id,
					title,
					verified,
					important_numbers,
					addition_id 
				FROM entities WHERE id = $1`

	if err := s.conn.QueryRow(ctx, query, id).Scan(
		&result.ID,
		&result.Title,
		&result.Verified,
		&result.ImportantNumbers,
		&result.AdditionID,
	); err != nil {
		return nil, err
	}

	return result, nil
}

func (s *storage) ChangeEntity(ctx context.Context, id int, additionID int, ent *entity.Entity, ad *entity.Addition) error {
	tx, err := s.conn.BeginTx(ctx, pgx.TxOptions{IsoLevel: pgx.ReadCommitted})
	if err != nil {
		return err
	}

	data := []interface{}{}

	entityQueryString := []string{}

	if ent.ImportantNumbers != nil {
		entityQueryString = append(entityQueryString, "important_numbers")
		data = append(data, ent.ImportantNumbers)
	}

	if ent.Title != nil {
		entityQueryString = append(entityQueryString, "title")
		data = append(data, ent.Title)
	}

	if ent.Verified != nil {
		entityQueryString = append(entityQueryString, "verified")
		data = append(data, ent.Verified)
	}

	var querySet string

	for i, v := range entityQueryString {
		querySet += fmt.Sprintf(`%s = $%d`, v, i+1)

		if !(i == len(entityQueryString)-1) {
			querySet += `, `
		}
	}

	var idAddition int

	queryEntity := fmt.Sprintf(`UPDATE entities SET %s WHERE id = %d RETURNING addition_id`, querySet, id)

	if err := tx.QueryRow(ctx, queryEntity, data...).Scan(&idAddition); err != nil {
		_ = tx.Rollback(ctx)
		return err
	}

	additionsQueryString := []string{}
	dataAdd := []interface{}{}

	if ad.AdditionalInfo != nil {
		additionsQueryString = append(additionsQueryString, "additional_info")
		dataAdd = append(dataAdd, ad.AdditionalInfo)
	}

	if ad.AdditionalNumber != nil {
		additionsQueryString = append(additionsQueryString, "additional_number")
		dataAdd = append(dataAdd, ad.AdditionalNumber)
	}

	var querySetAdditional string

	for i, v := range additionsQueryString {
		querySetAdditional += fmt.Sprintf(`%s = $%d`, v, i+1)

		if !(i == len(additionsQueryString)-1) {
			querySetAdditional += `, `
		}
	}

	queryAddition := fmt.Sprintf(`UPDATE additions SET %s WHERE id = %d`, querySetAdditional, idAddition)

	if len(additionsQueryString) > 0 {
		if _, err := tx.Exec(ctx, queryAddition, dataAdd...); err != nil {
			_ = tx.Rollback(ctx)
			return err
		}
	}

	if err := tx.Commit(ctx); err != nil {
		return err
	}

	return nil
}

func (s *storage) Create(ctx context.Context, ent *entity.Entity, ad *entity.Addition) (int, error) {
	tx, err := s.CreateTX(ctx)
	if err != nil {
		return 0, err
	}

	var idEntity int
	var idAddition int
	queryEntity := `INSERT INTO entities (title, verified, important_numbers) VALUES ($1, $2, $3) RETURNING id, addition_id`

	if err := tx.QueryRow(ctx, queryEntity, ent.Title, ent.Verified, ent.ImportantNumbers).Scan(&idEntity, &idAddition); err != nil {
		_ = tx.Rollback(ctx)
		return 0, err
	}

	if ad != nil {
		queryAdditional := `INSERT INTO additions (id, additional_info, additional_number) VALUES ($1, $2, $3)`

		if _, err := tx.Exec(ctx, queryAdditional, idAddition, ad.AdditionalInfo, ad.AdditionalNumber); err != nil {
			_ = tx.Rollback(ctx)
			return 0, err
		}
	}

	if err := tx.Commit(ctx); err != nil {
		_ = tx.Rollback(ctx)
		return 0, err
	}

	return idEntity, nil
}

func (s *storage) GetAll(ctx context.Context, filter entity.EntityFilter) ([]entity.EntityAddition, error) {

	var queryWhereString []string
	if filter.Title != nil {
		queryWhereString = append(queryWhereString, fmt.Sprintf(`e.title = '%s'`, *filter.Title))
	}

	if filter.Verified != nil {
		queryWhereString = append(queryWhereString, fmt.Sprintf(`e.verified = '%v'`, *filter.Verified))
	}

	var queryWhere string
	if len(queryWhereString) > 0 {
		queryWhere = `WHERE ` + strings.Join(queryWhereString, ` AND `)
	}

	var limit string
	var offset string
	if filter.PerPage != nil && filter.Page != nil {
		if *filter.PerPage > 0 {
			if *filter.Page == 0 || *filter.Page == 1 {
				offset = fmt.Sprintf("%d", 0)
			} else {
				offset = fmt.Sprintf("%d", (*filter.Page-1)**filter.PerPage)
			}

			limit = fmt.Sprintf(`LIMIT %d OFFSET %s`, *filter.PerPage, offset)
		}

	}

	// запрос на получение всех
	query := fmt.Sprintf(`SELECT * FROM entities e 
				LEFT JOIN additions a ON a.id = e.addition_id
				%s 
				ORDER BY e.id ASC
				%s`, queryWhere, limit)

	rows, err := s.conn.Query(ctx, query)
	if err != nil {
		return nil, err
	}

	defer rows.Close()

	result := []entity.EntityAddition{}

	for rows.Next() {
		var entityID int
		var title string
		var verified bool
		var importantNumbers []int
		var entityAdditionID int
		var additionID *int
		var additionalInfo *string
		var additionalNumber *int

		if err := rows.Scan(&entityID, &title, &verified, &importantNumbers, &entityAdditionID, &additionID, &additionalInfo, &additionalNumber); err != nil {
			return nil, err
		}

		ent := entity.EntityAddition{
			ID:       entityID,
			Title:    title,
			Verified: verified,
			Addition: entity.Addition{
				ID:               additionID,
				AdditionalInfo:   additionalInfo,
				AdditionalNumber: additionalNumber,
			},
			ImportantNumbers: importantNumbers,
		}

		result = append(result, ent)

	}

	return result, nil
}

func (s *storage) GetEntityByID(ctx context.Context, id int) (*entity.EntityAddition, error) {
	result := new(entity.EntityAddition)

	query := `SELECT 
					e.id,
					e.title,
					e.verified,
					e.important_numbers,
					a.id,
					a.additional_info,
					a.additional_number
			FROM entities e 
			LEFT JOIN additions a ON a.id = e.addition_id
			WHERE e.id = $1 LIMIT 1`

	if err := s.conn.QueryRow(ctx, query, id).Scan(
		&result.ID,
		&result.Title,
		&result.Verified,
		&result.ImportantNumbers,
		&result.Addition.ID,
		&result.Addition.AdditionalInfo,
		&result.Addition.AdditionalNumber,
	); err != nil {
		return nil, err
	}

	return result, nil
}

func (s *storage) DeleteEntityByID(ctx context.Context, id int) error {
	pg, err := s.conn.Exec(ctx, "DELETE FROM entities WHERE id = $1", id)
	if err != nil {
		return err
	}

	if pg.RowsAffected() == 0 {
		return fmt.Errorf("no rows found for this id")
	}

	return nil
}
