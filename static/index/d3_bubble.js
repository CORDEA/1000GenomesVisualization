function drawBubble(data) {
    
    var serArray = [];
    var chrList = ["chr1", "chr2", "chr3"];
    var list = [];


    for (var chr in chrList) {
        inObj = [chrList[chr], []]
            for (var keyS in data) {
                if (data[keyS][0] == chrList[chr]) {
                    inObj[1].push (
                            {'name': keyS, 'size': Number(data[keyS][1]) - 1000}
                            );
                }
            }
        serArray.push(inObj);
    }
    console.log(serArray)

    for (var keyS in serArray) {
        list.push({'name': serArray[keyS][0], 'children': serArray[keyS][1]});
    }

    var bArray = {'name': 'bubble', 'children': list};

    console.log(bArray)
    

    var svgWidth = 1000; // SVG$BNN0h$N2#I}(B
    var svgHeight = 1000;    // SVG$BNN0h$N=DI}(B
    var diameter = 1000; // $B0lHVBg$-$$1_$N%5%$%:(B
    var color = ["none", "#ffa0a0", "#a0a0ff", "orange", "#ffe090", "#a0ff90", "cyan", "#ccc", "#ff8080", "#c0ffc0", "#4090ff"];
    var svg = d3.select("#bubble").append("svg")
        .attr("width", svgWidth).attr("height", svgHeight)
    var bubble = d3.layout.pack()
        .size([diameter, diameter]) // $BI=<(%5%$%:$r;XDj(B
    var grp = svg.selectAll("g")    // $B%0%k!<%W$rBP>]$K$9$k(B
        .data(bubble.nodes(classes(bArray)))  // $B%G!<%?$rFI$_9~$`(B
        .enter()
        .append("g")
        .attr("transform", function(d) {    // $B1_$N(BX,Y$B:BI8$r@_Dj(B
            return "translate(" + d.x + "," + d.y + ")";
        })
    var circle = grp.append("circle")   // $B1_$r@8@.$9$k(B
        .attr("r", 0)   // $B1_$r;XDj$7$?H>7B$K$9$k(B
        .attr("fill", function(d,i){// $BEI$j$N?'$r;XDj(B
            for (var chr in chrList) {
                if (d.packageName == chrList[chr]) {
                    console.log(chrList[chr])
                    return color[Number(chr) + 1];
                }
            }
            return color[i]
        })
    var text = grp.append("text")   // $BJ8;z$r@8@.$9$k(B
        .attr("font-size", "9pt")   // $BJ8;z$N%5%$%:$r;XDj$9$k(B
        .attr("fill", "black")  // $BJ8;z$NEI$j$N?'$r;XDj$9$k(B
        .attr("opacity", 0) // $BITF)L@EY$r;XDj(B
        .style("text-anchor", "middle") // $B1_$N:BI8$NCf1{$+$iI=<($9$k$h$&$K$9$k(B
        .text(function(d) { return d.className; } ) // $B%G!<%?$NCf$N(BclassName$B$,CO6hL>$J$N$G!"$=$l$r=PNO(B
    // $B3,AX2=$5$l$?(BJSON$B%G!<%?$r%U%i%C%H2=$9$k(B (D3.js$BK\2H$N$r>/$7JQ99$7$FMxMQ(B)
    function classes(root) {
        var classes = [];
        function recurse(name, node) {
            if (node.children) node.children.forEach(function(child) { recurse(node.name, child); });
            else classes.push({packageName: name, className: node.name, value: node.size});
        }
        recurse(null, root);
        return {children: classes};
    }
    circle
        .transition()   // $B%H%i%s%8%7%g%s;XDj(B
        .duration(2000) // 2$BIC$+$1$F%"%K%a!<%7%g%s(B
        .attr("r", function(d){ // $B1_$r;XDj$7$?H>7B$K$9$k(B
            return d.r;
        })
    text
        .transition()   // $B%H%i%s%8%7%g%s;XDj(B
        .duration(2000) // 2$BIC$+$1$F%"%K%a!<%7%g%s(B
        .attr("opacity", 1.0)   // $BJ8;z$NITF)L@$r;XDj$9$k(B
}
