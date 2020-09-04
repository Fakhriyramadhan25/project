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
    $sql = "SELECT id, name, type, oneway, id_jalan_1, kode_traye, trayekalt, trayekalt2,
    trayekalt3, trayekalt4, trayekalt5, trayekalt6, trayekalt7, trayekalt8,
    trayekalt9, trayekalt1, trayekal_1, trayekal_2, trayekal_3, geom,
    source, target FROM trayekakhir order by name;";

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
