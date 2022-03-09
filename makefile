docs:
	cd docs
	make html
isort:
	isort src
	isort tests
	isort docs
typecheck:
	mypy src/enamlnative --ignore-missing-imports
lintcheck:
	flake8 --ignore=E501,W503 src
	flake8 --ignore=E501,W503 tests
	flake8 --ignore=E501,W503 docs
reformat:
	black src
	black tests
	black docs
test:
	pytest -v tests --cov src --cov-report xml --asyncio-mode auto

precommit: isort reformat lintcheck typecheck
