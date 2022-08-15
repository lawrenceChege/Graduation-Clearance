import json
import logging
from datetime import datetime, date

lgr = logging.getLogger(__name__)


def get_request_data(request):
	"""
	Retrieves the request data irrespective of the method and type it was send.
	@param request: The Django HttpRequest.
	@type request: WSGIRequest
	@return: The data from the request as a dict
	@rtype: QueryDict
	"""
	try:
		data = None
		if request is not None:
			request_meta = getattr(request, 'META', {})
			request_method = getattr(request, 'method', None)
			if request_meta.get('CONTENT_TYPE', '') == 'application/json':
				data = json.loads(request.body)
			elif str(request_meta.get('CONTENT_TYPE', '')).startswith('multipart/form-data;'):  # Special handling for
				# Form Data?
				data = request.POST.copy()
				data = data.dict()
			elif request_method == 'GET':
				data = request.GET.copy()
				data = data.dict()
			elif request_method == 'POST':
				data = request.POST.copy()
				data = data.dict()
			if not data:
				request_body = getattr(request, 'body', None)
				if request_body:
					data = json.loads(request_body)
				else:
					data = dict()
			return data
	except Exception as e:
		lgr.exception('get_request_data Exception: %s', e)
	return dict()


def normalize_date(date_text):
	"""
	Normalizes the date by converting it to a date time object
	@param date_text: The date string or instance to convert to a date object.
	@type date_text: str | datetime | date
	@return: The datetime converted accordingly.
	@rtype: datetime | None
	"""
	try:
		if isinstance(date_text, (datetime, date)):  # No need of processing
			return date_text
		valid_date_formats = [
			'%Y-%m-%d', '%Y/%m/%d', '%Y%m%d', '%d/%m/%Y', '%d-%m-%Y', '%d%m%Y', '%m/%d/%Y', '%m-%d-%Y', '%m%d%Y']
		for valid_date in valid_date_formats:
			try:
				return datetime.strptime(date_text, valid_date)
			except Exception:
				continue
	except Exception:
		pass
	return None


def generate_fixed_length_code(start_character: str = 'A', code: str = '1', filler: str = '0', length: int = 9) -> str:
	"""
	This generates a code of specified length
	@param start_character : Specify the character to start the code
	@type start_character: str
	@param code: The unique code to append
	@type code: str
	@param filler: The element to use as a filler
	@type filler: str
	@param length: To specify the length of the code
	@type length: int
	@return code : The alphanumeric code generated
	@type code: str
	"""
	length = length - len(start_character)
	code = code.rjust(abs(length), filler)
	return "{}{}".format(start_character, code)

