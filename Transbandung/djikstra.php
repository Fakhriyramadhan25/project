<?php
define("PG_DB"  , "transangkotbdg");
define("PG_HOST", "localhost");
define("PG_USER", "postgres");
define("PG_PASSWORD", "12345");
define("PG_PORT", "5433");
define("TABLE",   "trayekakhir");

function dijkstra($startPoint,$endPoint) {
        $dbcon = pg_connect("host=".PG_HOST." port=".PG_PORT." dbname=".PG_DB." user=".PG_USER." password=".PG_PASSWORD);
        $sql1 = "DROP TABLE IF EXISTS abcde";
        $sql2 = "DROP TABLE IF EXISTS hasildijkstra";
        $sql3 = "CREATE TABLE abcde AS SELECT * FROM pgr_dijkstra(
            'SELECT id, source, target, cost, reverse_cost FROM trayekakhir',
            $startPoint, $endPoint, false);";
        $sql4 = "CREATE TABLE hasildijkstra as select
        a.seq, a.edge, a.cost, b.geom, b.name, b.kode_traye, b.trayekalt, b.trayekalt2, b.trayekalt3,
        b.trayekalt4, b.trayekalt5, b.trayekalt6,
        b.trayekalt7, b.trayekalt8, b.trayekalt9, b.trayekalt1, b.trayekal_1, b.trayekal_2, b.trayekal_3
        from abcde as a left join trayekakhir
         as b on b.id = a.edge";

        $sql5 = "SELECT * from hasildijkstra order by seq;";

        $query1 = pg_query($dbcon,$sql1);
        $results1 = pg_fetch_all($query1);

        $query2 = pg_query($dbcon,$sql2);
        $results2 = pg_fetch_all($query2);

        $query3 = pg_query($dbcon,$sql3);
        $results3 = pg_fetch_all($query3);

        $query4 = pg_query($dbcon,$sql4);
        $results4 = pg_fetch_all($query4);

        $query5 = pg_query($dbcon, $sql5);
        $results5 = pg_fetch_all($query5);

        return $results5;
    }

try{
    $method_name=$_SERVER["REQUEST_METHOD"];
    if($_SERVER["REQUEST_METHOD"])
    {

        switch ($method_name)
        {
            case 'GET':

            case 'POST':
                $json = file_get_contents('php://input');
                $data = json_decode($json);
                $gidAwal = $data->awal;
                $gidAkhir = $data->akhir;
                $dijkstra = dijkstra($gidAwal,$gidAkhir);
                break;

            case 'PUT':

            case 'DELETE':
        }
        echo json_encode($dijkstra);
    }
    else{
        $dijkstra=array("status"=>"0","message"=>"Please enter proper request method !! ");
        echo json_encode($dijkstra);
    }

}
catch(Exception $e) {
     echo 'Caught exception: ',  $e->getMessage(), "\n";
}

?>
