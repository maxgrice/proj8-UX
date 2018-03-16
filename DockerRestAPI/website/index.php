<html>
    <head>
        <title>Brevet Times</title>
    </head>

    <body>
        <h1>Brevet Time Listings</h1>
        <ul>
            <?php
            $json = file_get_contents('http://laptop-service/listAll');
            echo "   All Times:\n";
            echo "\n";
            $obj = json_decode($json);
            $Opens = $obj->$open_times;
            $Closes = $obj->$close_times;           
            echo "   OPEN Times:\n";
            #echo $all;
            
            foreach ($Opens as $time) {
	            echo "<li>$time</li>";
	        }
	        echo "   Close Times:\n";
	        #echo $Closes;
	        
            foreach ($Closes as $time) {
	            echo "<li>$time</li>";
	        }
	        
	        $json = file_get_contents('http://laptop-service/listAll/json');
	        echo "   All Times (JSON):\n";
            $obj = json_decode($json);
            echo $obj;
            echo $Opens;
            $Opens = $obj->$open_times;
            $Closes = $obj->$close_times;           
            echo "   Open Times:\n";
            foreach ($Opens as $time) {
	            echo "<li>$time</li>";
	        }
	        echo "   Close Times:\n";
            foreach ($Closes as $time) {
	            echo "<li>$time</li>";
	        }
	 
	        $all_csv = file_get_contents('http://laptop-service/listAll/csv');
	        echo "   All Times (CSV):\n";
            echo $all_csv;
	        
	        $json = file_get_contents('http://laptop-service/listOpenOnly/json');
	        echo "   Open Times (JSON):\n";
            $obj = json_decode($json);
            $Opens = $obj->$open_times;          
            echo "   Open Times:\n";
            foreach ($Opens as $time) {
	            echo "<li>$time</li>";
	        }
	  
	        $json = file_get_contents('http://laptop-service/listCloseOnly/json');
	        echo "   Close Times (JSON):\n";
            $obj = json_decode($json);
            $Closes = $obj->$close_times;          
            echo "   Open Times:\n";
            foreach ($Closes as $time) {
	            echo "<li>$time</li>";
	        }
	
	        $open_csv = file_get_contents('http://laptop-service/listOpenOnly/csv');
	        echo "   Open Times (CSV):\n";
            echo $open_csv;
	  
	        $close_csv = file_get_contents('http://laptop-service/listCloseOnly/csv');
	        echo "   Close Times (CSV):\n";
            echo $close_csv;
	
            ?>
        </ul>
    </body>
</html>
