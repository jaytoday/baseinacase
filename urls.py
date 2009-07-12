def url_routes(map):

	#Public Views
	map.connect('', controller = 'views:Base')
	map.connect('/:user', controller = 'views:User')

