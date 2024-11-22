from typing import Dict, List, Optional, Union

from pydantic_yaml import YamlModel


class DateRange(YamlModel):
    start: str
    end: str


class ContactInfo(YamlModel):
    name: str
    objective: Optional[str]
    street_address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[str]
    phone: str
    email: str
    website: Optional[str]
    linkedin: Optional[str]
    github: Optional[str]

    @property
    def email_user(self):
        return self.email.split("@")[0]

    @property
    def email_domain(self):
        return self.email.split("@")[1]

    @property
    def first_name(self):
        return self.name[:-1]

    @property
    def last_name(self):
        return self.name[-1]

    @property
    def github_short(self):
        return self.github.replace("https://", "").replace("http://", "")

    @property
    def linkedin_short(self):
        return self.linkedin.replace("https://", "").replace("http://", "")


class Position(YamlModel):
    title: str
    date: Optional[DateRange]
    description: Optional[str]


class Employer(YamlModel):
    name: str
    date: Optional[DateRange]
    city: Optional[str]
    state: Optional[str]
    positions: Optional[List[Position]]


class Education(YamlModel):
    degree_date: str
    degree_name: str
    degree_concentration: str
    institution_url: Optional[str]
    institution_name: str
    institution_city: Optional[str]
    institution_state: Optional[str]


class Resume(YamlModel):
    contact_info: ContactInfo
    executive_summary: str
    qualifications: Union[Dict[str, List[str]], List[Dict]]
    employers: Optional[List[Employer]]
    other_work: Optional[List[Employer]]
    educations: Optional[List[Education]]
