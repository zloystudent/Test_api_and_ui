package entity

type Entity struct {
	ID               *int    `db:"id"`
	Title            *string `db:"title"`
	Verified         *bool   `db:"verified"`
	ImportantNumbers []int   `db:"important_numbers"`
	AdditionID       *int    `db:"addition_id"`
}

type EntityAddition struct {
	ID               int      `db:"id"`
	Title            string   `db:"title"`
	Verified         bool     `db:"verified"`
	Addition         Addition `db:"addition"`
	ImportantNumbers []int    `db:"important_numbers"`
}

type EntityFilter struct {
	Title    *string
	Verified *bool
	Page     *uint
	PerPage  *uint
}
