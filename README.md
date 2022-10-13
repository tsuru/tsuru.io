# tsuru.io website

This is the [tsuru.io](http://tsuru.io) landing page.

## Setting up

You must have the latest [Node.js](https://nodejs.org/) version installed.

After that, clone this project:

```shell
$ git clone git@github.com:tsuru/tsuru.io.git
```

Then install the dependencies:

```shell
$ cd tsuru.io
$ make install
```

This will install [SASS](http://sass-lang.com/) and [Grunt](http://gruntjs.com/getting-started) CLIs globally in your computer.

That's it. You're set.

## Running & developing

Having the dependencies installed, just run:

```shell
$ make run
```

Now you can access it locally at `localhost:7777`.
At any changes, the page will be automatically generated again.
