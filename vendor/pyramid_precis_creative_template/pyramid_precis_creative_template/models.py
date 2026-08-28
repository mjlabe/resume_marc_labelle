from typing import Dict, List, Optional, Union

from pydantic import Field
from pydantic_yaml import YamlModel


class DateRange(YamlModel):
    start: str
    end: str


class ContactInfo(YamlModel):
    first_name: str
    last_name: str
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
    def github_short(self):
        return self.github.replace("https://", "").replace("http://", "")

    @property
    def linkedin_short(self):
        return self.linkedin.replace("https://", "").replace("http://", "")


class Position(YamlModel):
    title: str
    employer: str
    date: DateRange
    description: str
    bullets: List[Union[str, Dict[str, str]]] = Field(default_factory=list)


class Education(YamlModel):
    degree_date: str
    degree_name: str
    degree_concentration: str
    institution_name: str


class Resume(YamlModel):
    contact_info: ContactInfo
    executive_summary: str
    qualifications: Union[Dict[str, List[str]], List[Dict]]
    positions: List[Position]
    educations: List[Education]
    zoom: Optional[str]
