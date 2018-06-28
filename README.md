# SHA2017 Badge Weather Status App

This App displays the weather outlook for the next 5 days using the buienradar weather API.

## Configuration

The app uses a buienradar specific location code which you'll need to obtain for your own location.
This can be done via the following url where you replace Delft with your own location.

https://api.buienradar.nl/data/search/1.0/?query=Delft&country=NL&locale=nl-NL

Returned is a JSON object which contains possibly multiple objects for your location, get the correct
location and extract the number id from the 'uri' value.

## Installing

Installation can be achieved with [mpfshell](https://github.com/wendlers/mpfshell).

1. Connect the badge
2. Open a serial connection and `import shell`
3. Close the connection
4. Start mpfshell

In mpfshell:

1. open ttyUSB0
2. cd /lib
3. md weekweather
4. cd weekweather
5. mput .*\.py
6. mput .*\.json
7. exit
