# Myhomelistings
DEPRECATED - That library is not being maintained anymore.

A library that enables programmatic interaction with [Myhome.ie](https://myhome.ie)
<!-- 
## Installation

daftlistings is available on the Python Package Index (PyPI). You can install daftlistings using pip.

``` bash
virtualenv env
source env/bin/activate
pip install myhomelistings
```

To install the development version, run:

``` bash
pip install https://github.com/AnthonyBloomer/daftlistings/archive/dev.zip
```

## Examples

Get apartments to let in Dublin City that are between €1000 and €1500 and contact the advertiser of each listing.

``` python
from daftlistings import Daft, RentType

daft = Daft()

daft.set_county("Dublin City")
daft.set_listing_type(RentType.APARTMENTS)
daft.set_min_price(1000)
daft.set_max_price(1500)

listings = daft.search()

if len(listings) > 0:
    first = listings[0]

    contact = first.contact_advertiser(
        name="Jane Doe",
        contact_number="019202222",
        email="jane@example.com",
        message="Hi, I seen your listing on daft.ie and I would like to schedule a viewing."
    )

    if contact:
        print("Advertiser contacted")
```

You can sort the listings by price, distance, upcoming viewing or date using the SortType object. The SortOrder object allows you to sort the listings descending or ascending.

``` python

from daftlistings import Daft, SortOrder, SortType, RentType

daft = Daft()

daft.set_county("Dublin City")
daft.set_listing_type(RentType.ANY)
daft.set_sort_order(SortOrder.ASCENDING)
daft.set_sort_by(SortType.PRICE)
daft.set_max_price(2500)

listings = daft.search()

for listing in listings:
    print(listing.formalised_address)
    print(listing.daft_link)
    print(listing.price)
    features = listing.features
    if features is not None:
        print('Features: ')
        for feature in features:
            print(feature)
    print("")

```

Parse listing data from a given search result url.

``` python

from daftlistings import Daft

offset = 0

while 1:
    daft = Daft()
    daft.set_result_url("https://www.daft.ie/dublin-city/new-homes-for-sale/?ad_type=new_development")
    daft.set_offset(offset)
    listings = daft.search()
    if not listings:
        break
    for listing in listings:
        print(listing.formalised_address)
        print(listing.price)
        print(' ')
    offset += 10

```

Find student accommodation near UCD that is between 850 and 1000 per month

``` python
from daftlistings import Daft, SortOrder, SortType, RentType, University, StudentAccommodationType

daft = Daft()
daft.set_listing_type(RentType.STUDENT_ACCOMMODATION)
daft.set_university(University.UCD)
daft.set_student_accommodation_type(StudentAccommodationType.ROOMS_TO_SHARE)
daft.set_min_price(850)
daft.set_max_price(1000)
daft.set_sort_by(SortType.PRICE)
daft.set_sort_order(SortOrder.ASCENDING)
daft.set_offset(offset)
listings = daft.search()

for listing in listings:
    print(listing.price)
    print(listing.formalised_address)
    print(listing.daft_link)

```

## Tests

The Python unittest module contains its own test discovery function, which you can run from the command line:

```
 python -m unittest discover tests/
``` -->

## Contributing

  - Fork the project and clone locally.
  - Create a new branch for what you're going to work on.
  - Push to your origin repository.
  - Create a new pull request in GitHub.
