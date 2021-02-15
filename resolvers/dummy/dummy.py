class Dummy:

    def __str__(self) -> str:
        return 'Test'

    def __call__(self, scheme) -> iter:
        """
        Returned meta should be valid scheme
        Process your data and populate scheme struct
        src/core/scheme/definition.py
        :param scheme: Scheme object
        :yield object: Scheme valid
        """
        yield scheme.validator.check([{
            "resource_id": 85,
            "imdb_code": "tt00000",
            "title": "A Fork in the Road",
            "year": 2010, "rating": 6, "runtime": 105,
            "genres": ["Action", "Comedy", "Crime"],
            "synopsis": "Baby loves have fun",
            "trailer_code": "uIrQ9535RFo",
            "language": "en",
            "small_image": {"url": "https://images-na.ssl-images-amazon.com/images/I/71-i1berMyL._AC_SL1001_.jpg"},
            "medium_image": {"url": "https://images-na.ssl-images-amazon.com/images/I/71-i1berMyL._AC_SL1001_.jpg"},
            "large_image": {"url": "https://images-na.ssl-images-amazon.com/images/I/71-i1berMyL._AC_SL1001_.jpg"},
            "date_uploaded_unix": 1446321498,
            "resource": [
                {
                    "cid": "QmVuR5s1enhtAK5ipvLNiqgSz8CecCkPL8GumrBE3e53gg",
                    "quality": "720p",
                    "index": "index.m3u8",
                    "type": "hls"
                }
            ]
        }], many=True)