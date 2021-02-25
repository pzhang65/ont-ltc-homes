# Ontario LTC Homes Dataset Generator

Generates a dataset containing most publicly reported data on Ontario Long-term Care Homes.


### Process:
* Access Ministry of Health's API to obtain list of LTC homes along with Ontario Ministry of Health Provider IDs (MOH_PRO_ID) and basic data i.e. address.
* Scrap http://publicreporting.ltchomes.net/ using MOH_PRO_ID as an query parameter.
* Combine results from API + scraps to generate dataset.
