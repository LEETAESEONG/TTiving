<template>
  <div>
    <b-container class="d-flex justify-content-between mb-2 pt-1">
      <b-button-group class="m-auto">
        <b-button @click="showMarkers(markers)" variant="outline-light"
          >표시하기</b-button
        >
        <b-button @click="hideMarkers(markers)" variant="outline-light"
          >감추기</b-button
        >
        <b-button @click="zoomOut" variant="outline-light">전체보기</b-button>
      </b-button-group>

      <div style="width: 70%" class="d-flex">
        <b-form-select
          class="rounded mx-1 p-1"
          style="background-color: black; color: white"
          v-model="selected"
          :options="options"
        >
        </b-form-select>
        <b-input-group>
          <b-form-input
            @keyup.enter.prevent="search"
            v-model="keyword"
            class="my-auto"
            style="background-color: black; color: white"
          ></b-form-input>
          <b-button @click="search" variant="outline-light"
            ><b-icon icon="search"></b-icon
          ></b-button>
        </b-input-group>
      </div>
    </b-container>
    <div id="map"></div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "MapView",
  components: {},
  data() {
    return {
      map: null,
      locations: null,
      markers: [],
      keyword: null,
      selected: null,
      options: [
        {
          text: "검색 카테고리",
          value: null,
        },
        {
          text: "영화명/촬영지명",
          value: 1,
        },
        {
          text: "촬영지 주소",
          value: 2,
        },
      ],
    };
  },
  mounted() {
    if (!window.kakao || !window.kakao.maps) {
      const script = document.createElement("script");
      script.src = `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${process.env.VUE_APP_KAKAOMAP_API_KEY}`;
      document.head.appendChild(script);
      script.addEventListener("load", () => {
         kakao.maps.load(() => {
        this.getData(); // getData 호출 후 initMap 실행
      });
      });
    } else {
      this.getData();
    }
  },
  methods: {
    handleError() {
      // 에러가 발생한 후에 호출되는 메서드
      window.location.reload();
    },
    search() {
      let results = [];
      console.log(this.selected);
      if (!this.selected) {
        alert("검색 카테고리를 선택해주세요.");
      } else {
        if (this.selected == 1) {
          this.locations.forEach((loc) => {
            if (loc.POI_NM.includes(this.keyword)) {
              results.push(loc);
            }
          });
        } else if (this.selected == 2) {
          this.locations.forEach((loc) => {
            let address = loc.CTPRVN_NM + loc.SIGNGU_NM + loc.LEGALDONG_NM;
            if (loc.LI_NM) {
              address += loc.LI_NM;
              if (loc.LNBR_NO) {
                address += loc.LNBR_NO;
              }
            } else if (loc.LNBR_NO) {
              address += loc.LNBR_NO;
            }
            // console.log(address)

            if (address.includes(this.keyword)) {
              results.push(loc);
            }
          });
        }

        // console.log(results);
        if (results.length != 0) {
          const bounds = new kakao.maps.LatLngBounds();

          this.hideMarkers(this.markers);
          for (let i = 0; i < results.length; i++) {
            this.createMarker(results[i]);
            bounds.extend(
              new kakao.maps.LatLng(results[i].LC_LA, results[i].LC_LO)
            );
          }
          this.map.setBounds(bounds);
        } else {
          alert("검색 결과가 존재하지 않습니다.");
        }
      }
    },
    initMap() {
      const container = document.getElementById("map");
      const options = {
        center: new kakao.maps.LatLng(36.00538, 127.55488),
        level: 13,
      };
      this.map = new kakao.maps.Map(container, options);

      this.locations.forEach((l) => {
        this.createMarker(l);
      });
    },
    showMarkers(data) {
      for (let i = 0; i < data.length; i++) {
        data[i].setMap(this.map);
      }
    },
    hideMarkers(data) {
      for (let i = 0; i < data.length; i++) {
        data[i].setMap(null);
      }
    },
    createMarker(loc) {
      const imageSrc = "https://cdn-icons-png.flaticon.com/256/412/412836.png",
        imageSize = new kakao.maps.Size(30, 34),
        imageOption = { offset: new kakao.maps.Point(27, 27) };

      const markerImage = new kakao.maps.MarkerImage(
          imageSrc,
          imageSize,
          imageOption
        ),
        markerPostion = new kakao.maps.LatLng(loc.LC_LA, loc.LC_LO);

      const marker = new kakao.maps.Marker({
        position: markerPostion,
        image: markerImage,
        clickable: true,
      });

      marker.setMap(this.map);

      this.markers.push(marker);

      let address = "";
      if (loc.LI_NM) {
        address += loc.LI_NM;
        if (loc.LNBR_NO) {
          address += loc.LNBR_NO;
        }
      } else if (loc.LNBR_NO) {
        address += loc.LNBR_NO;
      }
      const iwContent = `<div style="color:black; width:max-content" class="px-3">
          <div style="color:black; width:max-content;">${loc.POI_NM}</div>
          <div>
            ${loc.CTPRVN_NM} ${loc.SIGNGU_NM} ${loc.LEGALDONG_NM}
            <span>${address}</span>
          </div>
        </div>`;

      const infoWindow = new kakao.maps.InfoWindow({
        content: iwContent,
        removable: true,
      });

      kakao.maps.event.addListener(marker, "mouseover", () => {
        infoWindow.open(this.map, marker);
      });

      kakao.maps.event.addListener(marker, "mouseout", () => {
        infoWindow.close(this.map, marker);
      });

      kakao.maps.event.addListener(marker, "click", () => {
        const bounds = new kakao.maps.LatLngBounds();
        bounds.extend(marker.getPosition());
        this.map.setBounds(bounds);
      });
    },
    getData() {
      axios({
        url: "http://localhost:8000/movies/get_locations/",
        method: "GET",
      })
        .then((res) => {
          console.log(res);
          this.locations = res.data;
        })
        .then(() => {
          this.initMap();
        })
        .catch((err) => console.log(err));
    },
    zoomOut() {
      this.map.setCenter(new kakao.maps.LatLng(36.00538, 127.55488));
      this.map.setLevel(13);
    },
  },
};
</script>

<style>
#map {
  width: 100%;
  height: 780px;
}
</style>