APP = "secret-todolist"
DOMAIN = "secret-todolist.herokuapps.com"
PYTHON = "2.7"

def colorize(text, color)
  color_codes = {
    :black    => 30,
    :red      => 31,
    :green    => 32,
    :yellow   => 33,
    :blue     => 34,
    :magenta  => 35,
    :cyan     => 36,
    :white    => 37
  }
  code = color_codes[color]
  if code == nil
    text
  else
    "\033[#{code}m#{text}\033[0m"
  end
end

def virtual_env(command, env="env#{PYTHON}")
  sh "source #{env}/bin/activate && #{command}"
end

def create_virtual_env(dir, python)
  sh "virtualenv #{dir} -p #{python}"
end

task :clean => [] do
  sh "rm -rf ~*"
  sh "rm -rf *.pyc *.pyo"
  sh "rm -rf data/"
  sh "rm -rf *.egg-info"
  sh "rm -rf dist/"
end

task :install => [] do
  sh "python --version"
  sh "ruby --version"
  sh "easy_install pip"
  sh "brew install mongo"
  sh "brew install redis"
end

task :dev_env => [] do
  create_virtual_env("env#{PYTHON}", "python#{PYTHON}")
end

task :dependencies => [:dev_env] do
  envs = ["env#{PYTHON}"]
  envs.each { |env|
    virtual_env("pip install -r requirements.txt --upgrade --no-deps", "#{env}")
    virtual_env("pip install -r requirements-test.txt --upgrade --no-deps", "#{env}")
  }
end

task :tests => [] do
  virtual_env("nosetests", "env#{PYTHON}")
end

task :server => [] do
  virtual_env("foreman start")
end

task :mongo => [] do
  sh "mkdir -p data/db"
  sh "mongod --dbpath=data/db"
end

task :heroku_create => [] do
  sh "heroku apps:create #{APP}" if APP
  sh "heroku addons:add newrelic"
  # sh "newrelic-admin generate-config YOUR_ID newrelic.ini"
  sh "heroku addons:add papertrail"
  sh "heroku addons:add loggly"
  sh "heroku addons:add redistogo"
  sh "heroku addons:add mongohq"
  # sh "heroku addons:add mongolab"
  sh "heroku domains:add #{DOMAIN}" if DOMAIN
end

task :heroku => [] do
  sh "heroku login"
  sh "heroku config"

  sh "heroku ps:scale web=1"
  sh "heroku ps"
  sh "heroku open"
  sh "heroku logs"
  sh "heroku logs -t -p worker"
end

task :logs => [] do
  sh "heroku logs --tail"
end

task :console => [] do
  sh "heroku run python"
end

task :deploy => [] do
  sh "git push heroku master"
end

task :compress_js do
  sh "sudo npm install uglify-js -g"
  sh "uglifyjs static/js/*.js -o x.min.js --source-map x.min.js.map -p relative -c -m"
end

task :default => [:tests]
