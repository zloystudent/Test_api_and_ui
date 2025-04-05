package entity

type Addition struct {
	ID               *int    `db:"id"`
	AdditionalInfo   *string `db:"additional_info"`
	AdditionalNumber *int    `db:"additional_number"`
}
