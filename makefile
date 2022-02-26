docs:
	cd docs
	make html
isort:
	isort src
	isort tests
typecheck:
	mypy src --ignore-missing-imports
lintcheck:
	flake8 --ignore=E501 src
	flake8 --ignore=E501 tests
reformat:
	black src
	black tests
test:
	pytest -v tests --cov src --cov-report xml --asyncio-mode auto

precommit: isort reformat lintcheck typecheck
