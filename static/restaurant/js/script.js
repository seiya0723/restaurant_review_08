window.addEventListener("load" , function (){


    //マップの表示位置を指定(緯度・経度)
    var map = L.map('map').setView([34.6217684, -227.2109985], 9);

    //地図データはOSMから読み込み
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    for (let data of datas ){

        //ここでオリジナルのアイコンを作る
        let origin = L.icon({
            iconUrl: data["icon"],
            iconSize: [38, 38],
            iconAnchor: [19, 19],
            popupAnchor: [0, 0],
        });

        L.marker( [data["lat"], data["lon"]], {icon: origin } ).addTo(map).bindPopup(data["name"]).openPopup();
    }


});

