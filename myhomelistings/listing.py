from .request import Request
from .logger import Logger
import logging
import base64
import re
import html2text


class Listing(object):
    def __init__(self,
                 data_from_search=None,
                 url=None,
                 debug=False,
                 log_level=logging.ERROR):

        if(isinstance(data_from_search, str)):
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(data_from_search)
            data_from_search = soup.div

        self._data_from_search = data_from_search
        self._url = url
        self._debug = debug
        self._ad_page_content_data = None
        self._logger = Logger(log_level)

    @property
    def _ad_page_content(self):
        if(self._ad_page_content_data is not None):
            return self._ad_page_content_data

        if(self._url is not None):
            print('self._url')
            print(self._url)
            self._ad_page_content_data = Request(
                debug=self._debug).get(self._url)
        else:
            self._ad_page_content_data = Request(
                debug=self._debug).get(self.myhome_link)

        return self._ad_page_content_data

    @property
    def id(self):
        try:
            if(self._data_from_search):
                return ''.join(c for c in self._data_from_search['id'] if c.isdigit())
            else:
                return self._ad_page_content.find('div', {'class': 'propertyEnquiryAction'})['data-property-id']
        except Exception as e:
            if self._debug:
                self._logger.error(
                    "Error getting id. Error message: " + str(e))
            return

    @property
    def description(self):
        try:
            description_div = str(
                self._ad_page_content.find(
                    'div', {'class': 'active'}
                ).find('div', {'class': ['container']})
            )

            return html2text.html2text(description_div)
        except Exception as e:
            if self._debug:
                self._logger.error(
                    "Error getting description. Error message: " + str(e))
            return

    @property
    def agent_id(self):
        return

    @property
    def search_type(self):
        return

    @property
    def price(self):
        """
        This method returns the price.
        :return:
        """
        try:
            if(self._data_from_search):
                # todo
                return self._data_from_search.find('div', {'class': 'price'}).contents[0].strip()
            else:
                return self._ad_page_content.find('div', {'class': 'price'}).find('span').text
        except Exception as e:
            if self._debug:
                self._logger.error(
                    "Error getting price. Error message: " + str(e))
            return

    @property
    def price_change(self):
        return

    @property
    def upcoming_viewings(self):
        return

    @property
    def facilities(self):
        return

    @property
    def overviews(self):
        return

    @property
    def features(self):
        """
        This method returns the properties features.
        :return:
        """
        features = []
        try:
            features_p = str(
                self._ad_page_content.find(
                    'h4', text='Features').findNext('p').text
            )

            for item in features_p.split('•'):
                feat_str = item.strip().strip(',').strip('.')
                if(len(feat_str) > 0):
                    features.append(feat_str)
        except Exception as e:
            if self._debug:
                self._logger.error(
                    "Error getting features. Error message: " + str(e))
            return

        return features

    @property
    def formalised_address(self):
        """
        This method returns the formalised address.
        :return:
        """
        try:
            if(self._data_from_search):
                return self._data_from_search.find('div', {'class': 'result-bottom'}).find('h3').text  # todo
            else:
                return self._ad_page_content.find(
                    'div', {'class': 'address'}).text.strip()

        except Exception as e:
            if self._debug:
                self._logger.error(
                    "Error getting formalised_address. Error message: " + str(e))
            return

    @property
    def address_line_1(self):
        return

    @property
    def county(self):
        """
        This method returns the county name.
        :return:
        """
        formalised_address = self.formalised_address

        if formalised_address is None:
            return

        try:
            address = formalised_address.split(',')
            return address[-1].strip()
        except Exception as e:
            if self._debug:
                self._logger.error(
                    "Error getting county. Error message: " + str(e))
            return

    @property
    def images(self):
        """
        This method returns the listing image.
        :return:
        """
        try:
            div = self._ad_page_content.find(
                "div", {"id": "gallery"})['data-images']
        except Exception as e:
            if self._debug:
                self._logger.error(
                    "Error getting images. Error message: " + str(e))
            return
        images_list = []
        if div is None:
            return
        for item in div.split('|'):
            ret_str = item.strip().strip(',').strip('.')
            images_list.append(ret_str)

        return images_list

    @property
    def agent(self):
        """
        This method returns the agent name.
        :return:
        """
        return

    @property
    def agent_url(self):
        """
        This method returns the agent's url.
        :return:
        """
        return

    @property
    def contact_number(self):
        """
        This method returns the contact phone number.
        :return:
        """
        try:
            number = self._ad_page_content.find(
                'button', {'class': ['phone']}).find('a').text

            return number
        except Exception as e:
            if self._debug:
                self._logger.error(
                    "Error getting contact_number. Error message: " + str(e))
            return

    @property
    def myhome_link(self):
        """
        This method returns the url of the listing.
        :return:
        """
        try:
            if(self._data_from_search):  # todo
                link = self._data_from_search.find('a', href=True)
                return 'http://m.myhome.ie' + link['href']
            else:
                return self._ad_page_content.find('link', {'rel': 'canonical'})['href']
        except Exception as e:
            if self._debug:
                self._logger.error(
                    "Error getting daft_link. Error message: " + str(e))
            return

    @property
    def shortcode(self):
        """
        This method returns the shortcode url of the listing.
        :return:
        """
        try:
            id = self.id
            if id is None:
                return

            return 'https://m.myhome.ie/' + id
        except Exception as e:
            if self._debug:
                self._logger.error(
                    "Error getting shortcode. Error message: " + str(e))
            return

    @property
    def date_insert_update(self):
        """
        This method returns the shortcode url of the listing.
        :return:
        """
        try:
            div = self._ad_page_content.find(
                'div', {'class': 'addedTime'})
            index = [i for i, s in enumerate(
                div.contents) if 'Refreshed on' in str(s)][0] + 1
            return re.search("([0-9]{1,2}/[0-9]{1,2}/[0-9]{4})", str(div.contents[index]))[0]
        except Exception as e:
            if self._debug:
                self._logger.error(
                    "Error getting date_insert_update. Error message: " + str(e))
            return

    @property
    def views(self):
        """
        This method returns the "Property Views" from listing.
        :return:
        """
        return

    @property
    def dwelling_type(self):
        """
        This method returns the dwelling type.
        :return:
        """
        try:
            if(self._data_from_search):
                return self._data_from_search.find(
                    'i', {"class": "fa-home"}
                ).parent.text.strip()
            else:
                return self._ad_page_content.find(
                    'i', {"class": "fa-home"}
                ).parent.text.strip()

        except Exception as e:
            if self._debug:
                self._logger.error(
                    "Error getting dwelling_type. Error message: " + str(e))
            return

    @property
    def posted_since(self):
        """
        This method returns the date the listing was entered.
        :return:
        """
        
        return self.date_insert_update

    @property
    def bedrooms(self):
        """
        This method gets the number of bedrooms.
        :return:
        """
        try:
            if(self._data_from_search):
                return self._data_from_search.find(
                    'i', {"class": "fa-bed"}
                ).parent.text.strip()
            else:
                return self._ad_page_content.find(
                    'i', {"class": "fa-bed"}
                ).parent.text.strip()
        except Exception as e:
            if self._debug:
                self._logger.error(
                    "Error getting bedrooms. Error message: " + str(e))
            return

    @property
    def bathrooms(self):
        """
        This method gets the number of bathrooms.
        :return:
        """
        try:
            if(self._data_from_search):
                return self._data_from_search.find(
                    'i', {"class": "fa-bathtub"}
                ).parent.text.strip()
            else:
                return self._ad_page_content.find(
                    'i', {"class": "fa-bathtub"}
                ).parent.text.strip()

        except Exception as e:
            if self._debug:
                self._logger.error(
                    "Error getting bathrooms. Error message: " + str(e))
            return

    @property
    def city_center_distance(self):
        """
        This method gets the distance to city center, in km.
        :return:
        """
        
        return

    @property
    def transport_routes(self):
        """
        This method gets a dict of routes listed in Daft.
        :return:
        """
        
        return

    @property
    def latitude(self):
        """
        This method gets a dict of routes listed in Daft.
        :return:
        """
        try:
            return self._ad_page_content.find('div', {'id': 'brochure_map'})['data-lat']
        except Exception as e:
            if self._debug:
                self._logger.error(
                    "Error getting latitude. Error message: " + str(e))
            return None

    @property
    def longitude(self):
        """
        This method gets a dict of routes listed in Daft.
        :return:
        """
        try:
            return self._ad_page_content.find('div', {'id': 'brochure_map'})['data-lng']
        except Exception as e:
            if self._debug:
                self._logger.error(
                    "Error getting longitude. Error message: " + str(e))
            return None

    @property
    def ber_code(self):
        """
        This method gets ber code listed in Daft.
        :return:
        """
        try:
            
            ber_p = str(
                self._ad_page_content.find(
                    'h4', text='BER Details').findNext('p').text
            )

            return re.search("BER: (.*?)\s", str(ber_p))[1].lower()
        except Exception as e:
            if self._debug:
                self._logger.error(
                    "Error getting the Ber Code. Error message: " + str(e))
            return

    @property
    def commercial_area_size(self):
        """
        This method returns the area size. This method should only be called when retrieving commercial type listings.
        :return:
        """
        return

    @property
    def advertiser_name(self):
        """
        This method returns the area size. This method should only be called when retrieving commercial type listings.
        :return:
        """
        try:
            return self._ad_page_content.find('div', {'id': 'smi-negotiator-photo'}
                                              ).find('h2').text
        except Exception as e:
            if self._debug:
                self._logger.error(
                    "Error getting commercial_area_size. Error message: " + str(e))
            return 'N/A'

    @property
    def contact_info(self):
        """
        This method returns the area size. This method should only be called when retrieving commercial type listings.
        :return:
        """
        try:
            return self._ad_page_content.find('div', {'class': 'contactDetails'}
                                              ).find('h3').text.strip()
        except Exception as e:
            if self._debug:
                self._logger.error(
                    "Error getting commercial_area_size. Error message: " + str(e))
            return 'N/A'

    @property
    def group_id(self):
        """
        This method returns the area size. This method should only be called when retrieving commercial type listings.
        :return:
        """
        try:
            return self._ad_page_content.find('div', {'class': 'propertyEnquiryAction'}
                                              )['data-group-id']
        except Exception as e:
            if self._debug:
                self._logger.error(
                    "Error getting commercial_area_size. Error message: " + str(e))
            return 'N/A'

    def contact_advertiser(self, name, email, contact_number, message):
        """
        This method allows you to contact the advertiser of a listing.
        :param name: Your name
        :param email: Your email address.
        :param contact_number: Your contact number.
        :param message: Your message.
        :return:
        """

        req = Request(debug=self._debug)

        ad_search_type = self.search_type
        agent_id = self.agent_id
        ad_id = self.id

        response = req.post('https://myhome.ie/message/PropertyEnquiry', params={
            'propertyId': 'daft_contact_advertiser',
            'email': name,
            'name': email,
            'message': message,
            'phone': contact_number,
            'contactType': ad_search_type,
            'groupId': agent_id
        })

        if self._debug:
            self._logger.info("Status code: %d" % response.status_code)
            self._logger.info("Response: %s" % response.content)
        if response.status_code != 200:
            self._logger.error("Status code: %d" % response.status_code)
            self._logger.error("Response: %s" % response.content)
        return response.status_code == 200

    def as_dict(self):
        """
        Return a Listing object as Dictionary
        :return: dict
        """
        return {
            'search_type': self.search_type,
            'agent_id': self.agent_id,
            'id': self.id,
            'price': self.price,
            'price_change': self.price_change,
            'viewings': self.upcoming_viewings,
            'facilities': self.facilities,
            'overviews': self.overviews,
            'formalised_address': self.formalised_address,
            'address_line_1': self.address_line_1,
            'county': self.county,
            'listing_image': self.images,
            'agent': self.agent,
            'agent_url': self.agent_url,
            'contact_number': self.contact_number,
            'contact_info': self.contact_info,
            'advertiser_name': self.advertiser_name,
            'myhome_link': self.myhome_link,
            'shortcode': self.shortcode,
            'date_insert_update': self.date_insert_update,
            'views': self.views,
            'description': self.description,
            'dwelling_type': self.dwelling_type,
            'posted_since': self.posted_since,
            'num_bedrooms': self.bedrooms,
            'num_bathrooms': self.bathrooms,
            'city_center_distance': self.city_center_distance,
            'transport_routes': self.transport_routes,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'ber_code': self.ber_code,
            'commercial_area_size': self.commercial_area_size
        }

    def __repr__(self):
        return "Listing (%s)" % self.formalised_address
