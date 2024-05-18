from django.shortcuts import render
import sys
import folium
from folium import plugins
from folium.plugins import Search
from folium.plugins import FastMarkerCluster


# Create your views here.

def index(request):

	# Create the map
	folium_map = folium.Map(location=[61.1830809, -149.9170687], tiles='openstreetmap', zoom_start=12)	

	# Sample data
	place_name = "Some Account"
	additional_data = "Additional Data"
	salesforce_link = "<a href='https://www.salesforce.com' target='_blank'>Go to Salesforce</a>"


	# Popup
	popup_content = f"""
						<div>
							<h3><b>Some Account Name</b></h3>
							<h4>Account Type: Supplier</h4>
							<h5>
							Segmentation: High Interaction | Repeat Purchaser 
								<ul>
									<li>CY Margin: $1.23M</li>
									<li>Open Opportunities: $4.56M</li>
									<li>Win Rate: 78.9%</li>
									<li>Churn Risk: 12.3%</li>
								</ul>
								{salesforce_link}
							</h5>
						</div>
					   """


	folium.Marker(
		[61.19319, -149.86694],
		popup=folium.Popup(popup_content, max_width=300),
		tooltip='Click for details'
		).add_to(folium_map)

    # Convert for display in Django
	folium_map = folium_map._repr_html_()

	# tooltip popup for pins
	callback = (
                'function (row) {'
                        'var marker = L.marker(new L.LatLng(row[0], row[1]), {color: "red"});'
                        'var icon = L.AwesomeMarkers.icon({'
                        "icon: row[10],"
                        "iconColor: 'white',"
                        "markerColor: row[11],"
                        "prefix: 'glyphicon',"
                        "extraClasses: 'fa-rotate-0'"
                    '});'
                    'marker.setIcon(icon);'
                    "var popup = L.popup({maxWidth: '300'});"
                    "const account_name   = {text: row[2]};"
                    "const account_type   = {text: row[3]};"
                    "const ads_department = {text: row[4]};"
                    "const account_owner  = {text: row[5]};"
                    "const net_margin_3y  = {text: row[6]};"
                    "const net_margin_cy  = {text: row[7]};"
                    "const last_activity  = {text: row[8]};"
                    "const address        = {text: row[9]};"
                    "const account_guid   = {text: row[12]};"
                    "var mytext = $(`<div id='mytext' class='display_text' style='width: 100.0%; height: 100.0%;'> <h4> ${account_name.text} </h4> <br><b> ${account_type.text} <br> ${ads_department.text}</b> <br><br> Owned By: <b>${account_owner.text}</b><br>3Y NM: <b>${net_margin_3y.text}</b> <br>CY NM: <b>${net_margin_cy.text}</b> <br>Last Activity: <b>${last_activity.text}</b> <br>Next Visit: <b>-</b> <br><br> ${address.text} <br> <a href=\"https://adsinc.lightning.force.com/lightning/r/Account/${account_guid.text}/view\" target='blank'>View in Salesforce</a> <br> <a target='_blank' href=\"../account_insight/${account_guid.text}/\">Account Insights</a></div>`)[0];"
                    "popup.setContent(mytext);"
                    "marker.bindPopup(popup);"
                'return marker};'
                )


	context = {
				'map':  	folium_map,
				'testing':	'blah blah',

	}
	return render(request, 'dashboards/index.html', context)