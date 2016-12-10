function initViz() {
    var containerDiv = document.getElementById("followersViz"),
    url = "https://public.tableau.com/views/twit_tab/Sheet2?:embed=y&:display_count=yes;"
    var viz = new tableau.Viz(containerDiv, url);
}

function initViz2() {
    var containerDiv = document.getElementById("colorViz"),
    url = "https://public.tableau.com/views/twit_tab/Sheet1?:embed=y&:display_count=yes;"
    var viz = new tableau.Viz(containerDiv, url);
}
