# Converter
A Python 3.7 project that converts src_currency to dest_currency using data from the link:https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml
It can be run by typing "python API.py" in the command prompt window from Converter folder that you have downloaded to your local machine
or you can use for example Visual Studio to run it
In order for it to runn successfully before starting it you must install flask, flask_restful and wget on your machine, also port 5000 needs to be fre and available for the application
When the project starts you can get the result by sending a HTTP get request to the link:
http://localhost:5000/converter
with the Query Parameters being:
amount - the amount that you want to convert
src_currency - currency from which you are converting
dest_currency - currency you are converting to
reference_date - the date for which you want to do the conversion (rates on that date will be used for conversion)

Example: http://localhost:5000/converter?amount=10&src_currency=EUR&dest_currency=USD&reference_date=2020-03-23
