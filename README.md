# Unscrapulous - scrape unscrupulous entities
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)

![artwork](images/logo.png "Agent X who populates the database with unscrupulous entities")

*Artwork by [@xypnox](https://github.com/xypnox/)*

## Motivation
Various regulatory bodies publish list of people/entities who have violated laws or regulations. The primary identifier for these records are their PANs. Banks, brokers are supposed to not provide services to these entities, identified by their PANs. Unscrapulous is a python utility which has scrapers to create a huge database of such people/entities.

The PostgreSQL database `unscrupulous_entities` contains the following fields:
```
1. ID
2. PAN
3. Name
4. AddedDate (day of blacklisting according to the source)
5. Source
6. Meta (a JSON encoded field of whatever fields each source provides)
```

## Installation
```bash
$ sudo apt-get install postgresql postgresql-contrib libpq-dev
$ pip install unscrapulous
```

## Usage
```bash
$ unscrapulous --config=config.toml
```

## Development
```bash
$ git clone git@github.com:themousepotato/unscrapulous.git
$ cd unscrapulous
$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
$ poetry install
$ poetry build
$ pip install dist/unscrapulous-*.whl
```

## Config
The `config.toml` file has the following format:
```toml
[postgresql_conn]
host = 'localhost'
dbname = 'postgres'
user = 'postgres'
password = 'password'

[scrapers]
arbitration_awards_bse = false
arbitration_awards_nse = false
bse_defaulter_and_expelled_members = false
icex_defaulter_members = false
icex_expelled_members = false
income_tax_defaulters = false
irda_blacklisted = false
mca_company_defaulter_list = false
mca_director_defaulter_list = false
mca_director_disqualified_list = false
mca_proclaimed_offenders_ind = false
mcx_action_ap = false
mcx_defaulter_members = false
mcx_secretaries_defaulter_list = false
mse_arbitral_awards = false
ncdex_suspended_defaulted_expelled_debarred_members = false
nse_defaulted_members = false
nse_expelled_members = false
nse_regulatory_defaulting_clients = false
sebi_debarred_bse = true
sebi_debarred_nse = true
sfio_convicted = false
sfio_proclaimed_offenders = false
unsc_1988 = false
unsc_consolidated_list = false
wildlife_crime_convicts = false
```

## Popular users
|                               | Organization  | Description  |
| ----------------------------- |:-------------:|:-------------:
| ![](images/zerodha.png "Zerodha") | [Zerodha](https://zerodha.com/)  | Online platform to invest in stocks, derivatives, mutual funds, etc. |

## Roadmap
| Source                                                | Category      | Status        |
| ----------------------------------------------------- |:-------------:| :-------------|
| ACE Suspended Members                                 | A             | Couldn't find source |
| [Arbitration Awards - BSE](https://www.bseindia.com/investors/ArbitAwards.aspx)                              | A             | <ul><li>- [x] Scrape from source</li><li>- [ ] Generate fields for global csv</li></ul> |
| [Arbitration Awards - NSE](https://www1.nseindia.com/invest/dynaContent/arbitration_award.jsp?requestPage=main&qryFlag=yes)                              | A             | <ul><li>- [x] Scrape from source</li><li>- [ ] Generate fields for global csv</li></ul> |
| [BSE Defaulter and Expelled Members](https://www.bseindia.com/static/members/List_defaulters_Expelled_members.aspx)                    | A             | <ul><li>- [x] Scrape from source</li><li>- [ ] Generate fields for global csv</li></ul> |
| BSE Regulatory Defaulting Clients                     | A             | Couldn't find source |
| [ICEX Defaulter Members](https://www.icexindia.com/membership/expelled-defaulter-surrendered-members)                                | A             | <ul><li>- [x] Complete</li></ul> |
| [ICEX Expelled Members](https://www.icexindia.com/membership/expelled-defaulter-surrendered-members)                                 | A             | <ul><li>- [x] Complete</li></ul> |
| [MCX Action AP](https://www.mcxindia.com/membership/notice-board/notice-board-disciplinary-action)                                         | A             | <ul><li>- [x] Complete</li></ul> |
| [MCX Defaulter Members](https://www.mcxindia.com/Investor-Services/defaulters/list-of-clients-of-the-defaulter-members-apportioned-amount-not-claimed)                                 | A             | <ul><li>- [x] Complete</li></ul> |
| [MSE Arbitral Awards](https://www.msei.in/investors/list-of-arbitrators)                                   | A             | <ul><li>- [x] Scrape from source</li><li>- [ ] Generate fields for global csv</li></ul> |
| MSE Trading Clearing Members                          | A             | Couldn't find source |
| [NCDEX Suspended Defaulted Expelled Debarred Members](https://ncdex.com/suspended_member)   | A             | <ul><li>- [x] Scrape from source</li><li>- [ ] Generate fields for global csv</li></ul> |
| NMCE Defaulted Members                                | A             | Couldn't find source |
| NMCE Expelled Members                                 | A             | Couldn't find source |
| NMCE Suspended Members                                | A             | Couldn't find source |
| [NSE Defaulted Members](https://www1.nseindia.com/invest/content/defaulter_expld_memb.htm)                                 | A             | <ul><li>- [x] Complete</li></ul> |
| [NSE Expelled Members](https://www1.nseindia.com/invest/content/defaulter_expld_memb.htm)                                  | A             | <ul><li>- [x] Complete</li></ul> |
| [NSE Regulatory Defaulting Clients](https://www.nseindia.com/regulations/exchange-defaulting-clients)                     | A             | <ul><li>- [x] Complete</li></ul> |
| [UAPA](https://www.icsi.edu/uapa/)                                                  | A             | <ul><li>- [ ] Scrape from source</li><li>- [ ] Generate fields for global csv</li></ul> |
| [UNSC_1267/UNSC Consolidated List](https://www.un.org/securitycouncil/content/un-sc-consolidated-list)                      | A             | <ul><li>- [x] Complete</li></ul> |
| [UNSC_1988](https://www.un.org/securitycouncil/sanctions/1988/materials)                                             | A             | <ul><li>- [x] Complete</li></ul> |
| UNSC_2140                                             | A             | Couldn't find source |
| UNSC_2270                                             | A             | Couldn't find source |
| [SEBI Debarred - BSE](https://www.bseindia.com/investors/debent.aspx)                                   | A             | <ul><li>- [x] Complete</li></ul> |
| [SEBI Debarred - NSE](https://www.nseindia.com/regulations/member-sebi-debarred-entities)                                   | A             | <ul><li>- [x] Complete</li></ul>  |
|                                                       |               |               |
| [MCA Proclaimed Offenders (Ind)](http://www.mca.gov.in/MinistryV2/proclaimedoffenders.html)                        | B             | <ul><li>- [x] Scrape from source</li><li>- [ ] Generate fields for global csv</li></ul> |
| [SFIO Convicted](https://sfio.nic.in/sites/default/files/pdf/Conviction%20Matters%20from%202003.pdf)                                        | B             | <ul><li>- [x] Complete</li></ul> |
| [SFIO Proclaimed Offenders](https://sfio.nic.in/sites/default/files/pdf/Proclaimed%20Offenders%20Details%20DK%20Sabat.pdf)                             | B             | <ul><li>- [x] Complete</li></ul> |
| [RBI Suit File](https://suit.cibil.com/)                                         | B             | <ul><li>- [ ] Scrape from source</li><li>- [ ] Generate fields for global csv</li></ul> |
| [IRDA Blacklisted](https://agencyportal.irdai.gov.in/PublicAccess/BlackListedAgent.aspx)                                      | B             | <ul><li>- [x] Complete</li></ul>|
| [Income Tax Defaulters](http://office.incometaxindia.gov.in/administration/Pages/tax-defaulters.aspx)                                 | B             | <ul><li>- [x] Complete</li></ul> |
| [Wildlife Crime Convicts](http://wccb.gov.in/Content/Convicts.aspx)                               | B             | <ul><li>- [x] Complete</li></ul> |
| [MCA Director Defaulter List](http://www.mca.gov.in/MinistryV2/defaulterdirectorslist.html)                           | B             | <ul><li>- [x] Complete</li></ul> |
| [MCA Director Disqualified List](http://www.mca.gov.in/MinistryV2/disqualifieddirectorslist.html)                        | B             | <ul><li>- [x] Scrape from source</li><li>- [ ] Generate fields for global csv</li></ul> |
| [MCX Secretaries Defaulter List](https://www.mcxindia.com/Investor-Services/defaulters/defaulters-list)                        | B             | <ul><li>- [x] Complete</li></ul> |
| [NCLT (IBBI)](https://ibbi.gov.in/orders/nclt)                                           | B             | <ul><li>- [ ] Scrape from source</li><li>- [ ] Generate fields for global csv</li></ul> |
| [MCA Company Defaulters List](http://www.mca.gov.in/MinistryV2/defaultercompanieslist.html)                           | B             | <ul><li>- [x] Complete</li></ul> |
| European Union Sanctions                              | B             | Couldn't find source |
| [MCA Companies Struck Off list](http://www.mca.gov.in/MinistryV2/companies_stuckoff_248.html)                         | B             | <ul><li>- [ ] Scrape from source</li><li>- [ ] Generate fields for global csv</li></ul> |
| Interpol                                              | B             | Couldn't find source |
| [United Kingdom Sanction List](https://www.gov.uk/government/publications/the-uk-sanctions-list)                          | B             | <ul><li>- [ ] ods/odt -> csv</li><li>- [ ] Generate fields for global csv</li></ul> |
| OFAC                                                  | B             | Couldn't find source |
| Local PEP - Only India PEP                            | B             | Couldn't find source |




