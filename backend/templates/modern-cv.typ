#import "@preview/modern-cv:0.7.0": *

#show: resume.with(
  author: (
    firstname: "<< firstname >>",
    lastname: "<< lastname >>",
    email: "<< email >>",
    phone: "<< phone >>",
    github: "<< github >>",
    linkedin: "<< linkedin >>",
    address: "<< address >>",
    positions: (<% for pos in positions %>"<< pos >>", <% endfor %>),
  ),
  date: datetime.today().display(),
)

= Summary

<< summary >>

= Experience

<% for exp in experiences %>
#resume-entry(
  title: "<< exp.title >>",
  location: "<< exp.company >>",
  date: "<< exp.date >>",
  description: "<< exp.description >>"
)
<% endfor %>

= Education

<% for edu in education %>
#resume-entry(
  title: "<< edu.degree >>",
  location: "<< edu.institution >>",
  date: "<< edu.date >>",
  description: "<< edu.description >>"
)
<% endfor %>

= Skills

<% for skill in skills %>
- *<< skill.category >>*: << skill.skill_list >>
<% endfor %>

