use std::time::Duration;
use std::thread::sleep;
use std::error::Error;
use csv::Reader;
use sqlite::State;

fn main(){
    
    let time = Duration::from_secs(5);
    sleep(time);
    let connection = sqlite::open(":memory:").unwrap();
    let mut query = "
    CREATE TABLE inventory (Location TEXT, name TEXT, id TEXT, Count TEXT, Slots TEXT);
    ";
    connection.execute(query).unwrap();
    example();
    query = "
    SELECT * FROM inventory;";
    connection.execute(query).unwrap();

    let mut statement = connection.prepare(query).unwrap();
    
    while let Ok(State::Row) = statement.next() {
        println!("name = {}", statement.read::<String, _>("name").unwrap());
        println!("age = {}", statement.read::<i64, _>("age").unwrap());
    }
    
}
fn example() -> Result<(), Box<dyn Error>> {
    let mut rdr = csv::ReaderBuilder::new()
    .delimiter(b'\t')
    .from_path("Aliafriend-Inventory.txt")?;
    let connection = sqlite::open(":memory:").unwrap();
    let mut query = "";
    for result in rdr.records() {
    let record = result?;
    query ="INSERT INTO inventory VALUES {record}";
    connection.execute(query).unwrap();
    println!("{:?}", record);
    }
    Ok(())
}
//    let connection = sqlite::open(":memory:").unwrap();
 //   let query = "
 //   CREATE TABLE users (name TEXT, age INTEGER);
 //   INSERT INTO users VALUES('Alice', 42);
 //   INSERT INTO users VALUES('Bob', 26);
 //   ";
 //   connection.execute(query).unwrap();
 //   let query = "
  //  SELECT * FROM users;";
  //  connection.execute(query).unwrap();

  //  let mut statement = connection.prepare(query).unwrap();
    
  //  while let Ok(State::Row) = statement.next() {
  //      println!("name = {}", statement.read::<String, _>("name").unwrap());
  //      println!("age = {}", statement.read::<i64, _>("age").unwrap());
  //  }



