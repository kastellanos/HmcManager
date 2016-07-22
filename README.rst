About:
------

	This implementation make use of HmcRestClient https://github.com/PowerHMC/HmcRestClient project, the purpouse is generate reports of used memory and CPU of active partitions manageds by one HMC.

Disclaimer:
-----------
	These examples are shared as is and they are not formally supported by IBM or any of the authors and contributors. User assumes complete ownership and responsibility before modifying or executing them.

Installation:
-------------

    No installation needed.


Requirements:
-------------
	Power Hardware Management Console Version 8 Release 8.5

	Python Version >= 3.5.2

	**Python Libraries:**
	    Django>=1.9.7

            Used for interface the HmcRestApi implementation with a Web view.

        django-crispy-forms>=1.6.0

            Used to beautify Django forms

        numpy>=1.11.1

            Requested by pandas

        pandas>=0.18.1

            Proccess and generate report.

        XlsxWriter >= 0.9.3

            Convert pandas report to Excel.

		Requests version >= 2.10.0
			https://pypi.python.org/pypi/requests

			Used for processing HTTP requests and responses from the HMC.

		PyXB version = 1.2.4
			https://pypi.python.org/pypi/PyXB/

			Used for generating Python source code from HMC XSDs. The generated source code is used for processing UOM and PCM objects. If you upgrade HMC and if there is new schema version from HMC you may need to regenerate the source code to make it compatible with new version.

			Command to generate source code for UOM objects: ``python pyxbgen -u [UOM.xsd] -m [Output python file name e.g. UOM] --location-prefix-rewrite=platform:/resource/PMC.SCHEMA.UOM/tmp/build/schema=[Location of HMC schema]``

			Command to generate source code for PCM objects: ``python pyxbgen -u [ManagedSystemPcmPreference.xsd] -m [Output python file name e.g. ManagedSystemPcmPreferences]``

		feedparser version >= 5.2.1
			https://pypi.python.org/pypi/feedparser

			Used for processing Atom feed from the HMC.

Execution:
----------
    You need flush the DB before start django server in debug mode.

    ``python manage.py flush``

    Then you are ready to run the app in django debug mode.

    ``python manage.py runserver``


Reference to useful resources:
------------------------------

	PowerHMC developerworks community: https://www.ibm.com/developerworks/community/groups/community/powerhmc

	Link to PowerVM Python SDK: https://github.com/pypowervm/pypowervm