<?php
define("PG_DB"  , "transangkotbdg");
define("PG_HOST", "localhost");
define("PG_USER", "postgres");
define("PG_PASSWORD", "12345");
define("PG_PORT", "5433");
define("TABLE",   "trayekakhir");


function getAddresses() {
    $dbcon = pg_connect("host=".PG_HOST." port=".PG_PORT." dbname=".PG_DB.
    " user=".PG_USER." password=".PG_PASSWORD);
    $addresses = [];
    $sql = "SELECT id, kodetrayek, namatrayek, warna, notrayek
    FROM atribut;
  ";

    $query = pg_query($dbcon,$sql);

    $results = pg_fetch_all($query);

    return $results;
}


try{
    $method_name=$_SERVER["REQUEST_METHOD"];
    if($_SERVER["REQUEST_METHOD"])
    {

        switch ($method_name)
        {
            case 'GET':
                $data = getAddresses();
                break;

            case 'POST':

            case 'PUT':

            case 'DELETE':
        }
        echo json_encode($data);
    }
    else{
        $data=array("status"=>"0","message"=>"Please enter proper request method !! ");
        echo json_encode($data);
    }

}


catch(Exception $e) {
     echo 'Caught exception: ',  $e->getMessage(), "\n";
}

?>
