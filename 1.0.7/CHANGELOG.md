# UPDATE 1.0.7

## REMOVED

- `setup.cfg`
	- Fixed an issue where pip would try to install python built-in packages, resulting in an error, by removing those from the required packages.
		- `sys`, `time`, `random`

## CHANGED

- `setup.cfg`
	- Changed the required python version from `>= 3.10` to `>= 3.12`, since I'm upgrading to 3.12.1 everywhere.