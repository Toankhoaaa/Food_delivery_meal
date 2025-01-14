import 'package:flutter/foundation.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

import '../../common/color_extension.dart';
import '../../common_widget/round_textfield.dart';

class ChangeAddressView extends StatefulWidget {
  const ChangeAddressView({super.key});

  @override
  State<ChangeAddressView> createState() => _ChangeAddressViewState();
}

class _ChangeAddressViewState extends State<ChangeAddressView> {
  GoogleMapController? _controller;

  final List<LatLng> locations = const [
    LatLng(1.3521, 103.8198), // Singapore
    LatLng(3.1390, 101.6869), // Kuala Lumpur
    LatLng(-6.2088, 106.8456), // Jakarta
    LatLng(13.7563, 100.5018), // Bangkok
    LatLng(14.5995, 120.9842), // Manila
    LatLng(10.7769, 106.7009), // Ho Chi Minh City
  ];

  final List<String> labels = ["S", "K", "J", "B", "M", "H"];
  final List<Color> colors = [
    Colors.red,
    Colors.blue,
    Colors.green,
    Colors.orange,
    Colors.purple,
    Colors.cyan
  ];

  late Set<Marker> _markers;

  static const CameraPosition _initialCameraPosition = CameraPosition(
    target: LatLng(1.3521, 103.8198), // Singapore
    zoom: 4.5,
  );

  @override
  void initState() {
    super.initState();
    _markers = _createMarkers();
  }

  Set<Marker> _createMarkers() {
    Set<Marker> markers = {};
    for (int i = 0; i < locations.length; i++) {
      markers.add(
        Marker(
          markerId: MarkerId('marker-$i'),
          position: locations[i],
          icon: BitmapDescriptor.defaultMarkerWithHue(
            _getHueFromColor(colors[i]),
          ),
          infoWindow: InfoWindow(
            title: "Location ${labels[i]}",
            snippet: "Customized marker at ${locations[i]}",
          ),
        ),
      );
    }
    return markers;
  }

  double _getHueFromColor(Color color) {
    return HSVColor.fromColor(color).hue;
  }

  Widget _buildCustomMarker(String text, Color color) {
    return Container(
      padding: const EdgeInsets.all(5),
      decoration: BoxDecoration(
        color: color,
        shape: BoxShape.circle,
      ),
      child: Center(
        child: Text(
          text,
          style: const TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: TColor.white,
        leading: IconButton(
          onPressed: () {
            Navigator.pop(context);
          },
          icon: Image.asset("assets/img/btn_back.png", width: 20, height: 20),
        ),
        title: Text(
          "Change Address",
          style: TextStyle(
            color: TColor.primaryText,
            fontSize: 20,
            fontWeight: FontWeight.w800,
          ),
        ),
      ),
      body: Stack(
        children: [
          GoogleMap(
            mapType: MapType.normal,
            initialCameraPosition: _initialCameraPosition,
            markers: _markers,
            gestureRecognizers: Set()
              ..add(Factory<PanGestureRecognizer>(
                    () => PanGestureRecognizer(),
              )),
            onMapCreated: (GoogleMapController controller) {
              _controller = controller;
            },
          ),
          Positioned(
            bottom: 20,
            left: 10,
            right: 10,
            child: Column(
              children: [
                Padding(
                  padding:
                  const EdgeInsets.symmetric(vertical: 10, horizontal: 25),
                  child: RoundTextfield(
                    hintText: "Search Address",
                    left: Icon(Icons.search, color: TColor.primaryText),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 25),
                  child: Row(
                    children: [
                      Image.asset('assets/img/fav_icon.png',
                          width: 35, height: 35),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          "Choose a saved place",
                          style: TextStyle(
                              color: TColor.primaryText,
                              fontSize: 14,
                              fontWeight: FontWeight.w600),
                        ),
                      ),
                      Image.asset(
                        'assets/img/btn_next.png',
                        width: 15,
                        height: 15,
                        color: TColor.primaryText,
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
