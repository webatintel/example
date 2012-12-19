def main():
	try:
		import gyagp
		gyagp.check()
	except ImportError:
		print('Module sparrow has not been installed')
		
	try:
		from gyagp import module
		module.check()
	except ImportError:
		print('Module sparrow has not been installed')		
		
if __name__ == "__main__":
    main()
