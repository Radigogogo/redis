package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/go-redis/redis"
	"github.com/gorilla/mux"

	_ "github.com/denisenkom/go-mssqldb"
)

type DB struct {
	redis *redis.Client
	mssql *sql.DB
}

func NewDB() *DB {

	opt := &redis.Options{
		Addr:     "192.168.81.99:6379",
		Password: "",
		DB:       0,
	}

	client := redis.NewClient(opt)
	pong, err := client.Ping().Result()
	if err != nil {
		log.Panic(err, pong)
	}

	db, err := sql.Open("mssql", "server=192.168.81.99;user id=Radi;password=phison;database=TIC_DB")
	if err != nil {
		log.Panic(err)
	}

	return &DB{redis: client, mssql: db}
}

type Table struct {
	TL_ID             string `json:"TL_ID"`
	Tester_ID         string `json:"Tester_ID"`
	Test_Status       string `json:"Test_Status"`
	Running_StartTime string `json:"Running_StartTime"`
	Test_End_Time     string `json:"Test_End_Time"`
	Test_Result       string `json:"Test_Result"`
	Test_Status_2     string `json:"Test_Status_2"`
	Tool_Name         string `json:"Tool_Name"`
	Tool_Version      string `json:"Tool_Version"`
	Pattern_Result    string `json:"Pattern_Result"`
	Pattern_Name      string `json:"Pattern_Name"`
	Pattern_Duration  string `json:"Pattern_Duration"`
}

func homePage(w http.ResponseWriter, r *http.Request) {

	fmt.Fprintf(w, "Hello World!")

}

func (d *DB) returnRedisAll(w http.ResponseWriter, r *http.Request) {

	w.Header().Set("Content-Type", "application/json;charset=UTF-8")

	vars := mux.Vars(r)
	keyID := vars["id"]
	val, err := d.redis.Get(keyID).Result()
	if err != nil {
		// Do Logical Here to Select data From Database
		// And Set the Value from Database to Redis
		// Set Expiration to 5 second

		data := d.getData()
		j, err := json.Marshal(data)
		if err != nil {
			log.Panic(err)
		}
		err = d.redis.Set(keyID, j, 5*time.Second).Err()
		if err != nil {
			log.Panic(err)
		}

		// Send The Headers and Payload
		fmt.Println("MISS AND GET FROM DB")
		json.NewEncoder(w).Encode(data)
		return
	}

	// Send The Headers and Payload value From Redis Cache
	fmt.Println("HIT AND GET FROM REDIS")
	w.Write([]byte(val))

}

func (d *DB) getData() []*Table {
	rows, err := d.mssql.Query(`
	with 
	tt as(
	SELECT TOP(10)
	TK.TL_ID,
	ISNULL(TK.Tester_ID, 0) as Tester_ID,
	TK.Test_Status,
	ISNULL(Running_StartTime,0) as Running_StartTime, 
	Test_End_Time,
	(SELECT Name1 FROM dbo.VRs_View_Code_Describe WHERE System = 'VRS' AND Type = '101' AND Code = TK.Test_Result) AS Test_Result,
	(SELECT Name1 FROM dbo.VRs_View_Code_Describe WHERE System = 'VRS' AND Type = '100' AND Code = TK.Test_Status) AS Test_Status_2,
	Tool_Name,
	Tool_Version,
	ISNULL(PT.Test_Result,0) AS Pattern_Result,
	ISNULL(PT.Pattern_Name, 0) as Pattern_Name,
	ISNULL(PT.Test_Duration,0) AS Pattern_Duration
	FROM dbo.VRs_View_Base_Task AS TK
	LEFT JOIN dbo.Tool_List TL ON TK.TL_ID = TL.TL_ID
	LEFT JOIN dbo.Pattern_List PT ON TK.TK_ID = PT.TK_ID
	)

	Select * 
	from  tt 
	`)
	if err != nil {
		panic(err)
	}
	defer rows.Close()

	pls := make([]*Table, 0)

	for rows.Next() {
		pl := new(Table)
		if err := rows.Scan(&pl.TL_ID, &pl.Tester_ID, &pl.Test_Status, &pl.Running_StartTime, &pl.Test_End_Time, &pl.Test_Result, &pl.Test_Status_2, &pl.Tool_Name, &pl.Tool_Version, &pl.Pattern_Result, &pl.Pattern_Name, &pl.Pattern_Duration); err != nil {
			panic(err)
		}
		pls = append(pls, pl)
	}
	if err := rows.Err(); err != nil {
		panic(err)
	}
	return pls
}

func (d *DB) returnAll(w http.ResponseWriter, r *http.Request) {

	w.Header().Set("Content-Type", "application/json;charset=UTF-8")
	json.NewEncoder(w).Encode(d.getData())
}

func main() {

	db := NewDB()

	myRouter := mux.NewRouter().StrictSlash(true)
	myRouter.HandleFunc("/", homePage)
	myRouter.HandleFunc("/demo", db.returnAll)
	myRouter.HandleFunc("/demo-redis", db.returnRedisAll)
	log.Fatal(http.ListenAndServe(":80", myRouter))
}
