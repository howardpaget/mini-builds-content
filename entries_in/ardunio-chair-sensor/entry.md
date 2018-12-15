## Set up the solution

First things first, let's create an ASP.NET web api using the `dotnet new` command:
~~~
dotnet new webapi -n ResistorColoursApi
~~~

Next we'll create a lib to contain the logic to parse resistor color bands and a test project to contain our unit tests:
~~~
dotnet new classlib -n ResistorColoursLib
dotnet new xunit -n ResistorColoursTest
~~~

Finally, we'll create a solution and tie all the projects together in that solution:
~~~
dotnet new sln
dotnet sln add ResistorColoursLib ResistorColoursApi ResistorColoursTest
~~~

## Run the API

To check that the solution has been setup correctly we can build the api project:

~~~
dotnet build --project ResistorColorsApi\\
~~~

And navigate to http://localhost:5000/api/values. If you see some JSON everything is working as expected.

## Deploy on Google App Engine

Create a app.yaml file containing the lines below in the ResistorColoursApi folder. 

~~~
runtime: aspnetcore
env: flex
~~~

Add the yaml file to the api project by updating ResistorColorsApi.csproj:
~~~
<Project ...>
...
<ItemGroup> 
    <None Include=\"app.yaml\" CopyToOutputDirectory=\"PreserveNewest\" />
</ItemGroup>
...
</Project>
~~~

Publish the solution:
~~~
dotnet publish -c Release
~~~

Create and deploy the solution to Google App Engine:
~~~
gcloud projects create resistor-bands
gcloud config set project resistor-bands
gcloud app create
gcloud app deploy .\\bin\elease\\netcoreapp2.1\\publish\\app.yaml
gcloud app browse
~~~

## Delete the project from Google App Engine

Having an app running on Google App Engine costs a few dollars per month so you may want to delete it before get charged this can be done with the command below:

~~~
gcloud projects delete resistor-bands
~~~","snippet":"Let's build a web api to iterpret resistor colour bands in ASP.NET Core