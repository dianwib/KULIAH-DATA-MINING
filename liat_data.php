<!DOCTYPE html>
<html>
<head>
   <title></title>
</head>
<body>
<form action="" method="POST" >
<center>
   <table border="2px" >
   <th >NO</th>
   
   <th >MERK</th>
   <th >MODEL</th>
   <th >TIPE</th>   
   <th >TAHUN</th>   
   <th >WARNA</th>
   <th >DEALER</th>
   <th >HARGA</th>
   <th >KOTA</th>
   <th >PROVINSI</th>
   <th >DESKRIPSI</th>

   <?php

   class MyDB extends SQLite3 {
      function __construct() {
         $this->open('otomart.db');
      }
   }
   
   $db = new MyDB();
   if(!$db) {
      echo $db->lastErrorMsg();
   } else {
      echo "Opened database successfully\n";
   }

   $sql =<<<EOF
      SELECT * from mobil_bekas;
EOF;


   $ret = $db->query($sql);
   $no_urut=1;
   while($row = $ret->fetchArray(SQLITE3_ASSOC) ) {
      echo "<tr>";
         echo "<td>". $no_urut ."</td>";
         
         echo "<td>". $row['merk'] ."</td>";
         echo "<td>". $row['model'] ."</td>";
         echo "<td>". $row['tipe'] ."</td>";
         echo "<td>". $row['tahun'] ."</td>";
         echo "<td>". $row['warna'] ."</td>";
         echo "<td>". $row['showroom'] ."</td>";
         echo "<td>". $row['harga'] ."</td>";
         echo "<td>". $row['kota'] ."</td>";
         echo "<td>". $row['provinsi'] ."</td>";
         echo "<td>". $row['deskripsi'] ."</td>";
         echo "</tr>";
         $no_urut+=1;
         }
   echo "</table></form>";
   echo "Operation done successfully\n";
   $db->close();
?>