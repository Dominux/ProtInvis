chart.on('plotly_click', function(data){
    let pts = '';
    for (let i=0; i < data.points.length; i++){
        pts = data.points[i].text;
    }
    window.open('https://www.uniprot.org/uniprot/'+pts, '_blank');
});
