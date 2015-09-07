<html>
<head>
<script type="text/javascript"
  src="dygraph-combined.js"></script>
 
</head>
<body>
<img src="ffbs.svg" align="right" width="20%"> 
<div id="graphdiv2" style="width:95%; height:70%;"></div>
<script type="text/javascript">
  g2 = new Dygraph(
    document.getElementById("graphdiv2"),
    "/out/<?php echo $_GET['hash'] . date("Ym") ?>.csv", // path to CSV file
    {
	//xValueFormatter: Dygraph.dateString_,
	//xTicker: Dygraph.dateTicker,
	digitsAfterDecimal: 3,
	labelsKMB: true,
	drawAxesAtZero: true,
	title: 'Clients auf Router',
	xlabel: 'Zeitpunkt [UTC]',
	ylabel: 'Clients',
	connectSeparatedPoints: true
	
}          // options
  );
</script><br>
</body>
</html>
