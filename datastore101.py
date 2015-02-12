#!/usr/bin/env python
#
# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import datetime

import jinja2
import webapp2
from google.appengine.ext import ndb


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Conference(ndb.Model):
    title = ndb.StringProperty()
    city = ndb.StringProperty()
    start_date = ndb.DateProperty(indexed=False)
    end_date = ndb.DateProperty(indexed=False)
    max_attendees = ndb.IntegerProperty()


class MainPage(webapp2.RequestHandler):
    def get(self):
        conference_values = {
            "conferences": Conference.query().order(Conference.title)}
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(conference_values))


class CreateConference(webapp2.RequestHandler):
    def post(self):
        conference = Conference()
        conference.title = self.request.get('title')
        conference.city = self.request.get('city')
        conference.start_date = datetime.datetime.strptime(self.request.get(
            'startdate'), '%Y-%m-%d').date()
        conference.end_date = datetime.datetime.strptime(self.request.get(
            'enddate'), '%Y-%m-%d').date()
        conference.max_attendees = int(self.request.get('maxAttendees'))
        conference.put()
        self.redirect('/')

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/create', CreateConference),
], debug=True)
