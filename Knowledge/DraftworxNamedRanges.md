| NamedRange | Detail |
| --- | --- |
| Director_board | Used to reference the accurate term for the board of directors of the entity. In this case, Director_board evaluates to “director” because there is only a single director included in the client setup (or default to director if client setup not populated yet). Once 2 or more directors have been included in client setup then this named range will evaluate to “directors”. |
| Director_is_are | used to accurately use the word is or are depending whether there is only a single director or multiple directors. eg. the director is VS the directors are. |
| ApplicableAct | The Applicable Companies Act legislation that is applicable to the entity depending on it’s country of incorporation. In South Africa this is the “Companies Act of South Africa”. This should be dynamically updated depending on the country that is selected which is captured in the Country namedrange which in this example has a value of “South Africa” |
| AFS_Name | The name of the financial statements which is configurable in the client setup. Used throughout the financial statements to reference the document. In this example the value is “Annual Financial Statements”. |
| DisclosureType | The disclosure type is is the accounting standard that is applied to these financials / accounting framework applied. In this example this is “IFRS”. |
| DGender_their | a named range used to construct grammatically correct sentences depending on the gender of the directors and whether the Director_board is singular or plural.  |
| GroupAFSPrefix | If the AFS are for a group then the GroupAFSPrefix will include the word “consolidated” other wise it is just blank. |
| GroupEntityCase | In this example this evaluates to “company” because this is for a single entity’s financials otherwise it would evaluate to “group” |
| Finyear_Monthfinperiod | evalutes to “financial year” or could be for months if doing management accounts. |
