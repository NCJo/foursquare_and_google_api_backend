from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stderr = codecs.getwriter('utf-8')(sys.stderr)

# SET UP
foursquare_client_id = "GQKIB0QDCNIL0VVN13KLA2JIULCFJM3PDXI41WOIEY234QIP"
foursquare_client_secret = "4MTFDZVSW50LFAR31IGYH5M4MWSRX5TO1GOTJDIUFR2H3SYB"

# Converted JSON formatted of first result from all results

def findARestaurant(mealType, location):
    #1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
    coordinate = getGeocodeLocation(location)

	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
	#HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
    date = "20180402"

    #3. Grab the first restaurant
    url = 'https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&ll=%s&query=%s&v=%s' % (foursquare_client_id, foursquare_client_secret, coordinate, mealType, date)

    h = httplib2.Http()
    response, content = h.request(url, 'GET')
    result = json.loads(content)
    """
    # verified
    # name
    # referralId
    # venueChains
    # url
    # hereNow
    # specials
    # allowMenuUrlEdit
    # contact
    # hasPerk
    # location
    # beenHere
    # stats
    # id
    # categories
    """
    if result['response']['venues']:
        restaurant = result['response']['venues'][0]

        venue_id = restaurant['id']
        restaurant_name = restaurant['name']
        restaurant_address = restaurant['location']['formattedAddress']
        address = ""
        for i in restaurant_address:
            address += i + " "
        restaurant_address = address

    	#4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
        url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&v=20150603&client_secret=%s' % ((venue_id,foursquare_client_id,foursquare_client_secret)))
        result = json.loads(h.request(url, 'GET')[1])
        #5.  Grab the first image
        if result['response']['photos']['items']:
            firstpic = result['response']['photos']['items'][0]
            prefix = firstpic['prefix']
            suffix = firstpic['suffix']
            imageURL = prefix + "300x300" + suffix
        else:
            #6.  if no image available, insert default image url
            imageURL = "http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct"

        #7. Return a dictionary containing the restaurant name, address, and image url
        restaurantInfo = {'name':restaurant_name, 'address':restaurant_address, 'image':imageURL}
        print "Restaurant Nmae: %s" % restaurantInfo['name']
        print "Restaurant Address %s" % restaurantInfo['address']
        print "Restaurant Image %s" % restaurantInfo['image']
        return restaurantInfo
    else:
        print "No Restaurants Found for %s" % location
        return "No Restaurants Found"


if __name__ == '__main__':
    findARestaurant("Pizza", "Tokyo, Japan")
    findARestaurant("Tacos", "Jakarta, Indonesia")
    findARestaurant("Tapas", "Maputo, Mozambique")
    findARestaurant("Falafel", "Cairo, Egypt")
    findARestaurant("Spaghetti", "New Delhi, India")
    findARestaurant("Cappuccino", "Geneva, Switzerland")
    findARestaurant("Sushi", "Los Angeles, California")
    findARestaurant("Steak", "La Paz, Bolivia")
    findARestaurant("Gyros", "Sydney Australia")
