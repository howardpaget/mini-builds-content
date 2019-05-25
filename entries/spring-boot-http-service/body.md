## Introduction

Spring Boot is a lightweight Java framework for building standalone web applications and micros services. In this article we will build a simple 'clicker' app that is an app the keeps track of ho many times a button was clicked. We will cover handling different request methods (GET and POST) and providing static content.

## GitHub Repo

The code can be found here https://github.com/mini-builds/spring-boot-clicker.

## Gradle Build Script

Below is a minimal `build.gradle` file that pulls in all the required dependencies and tasks. The `bootJar` task builds a jar bundled with a Tomcat server i.e. a uber/fat jar that you can run using `java -jar file.jar`.

```groovy
buildscript {
    repositories {
        mavenCentral()
    }
    dependencies {
        classpath("org.springframework.boot:spring-boot-gradle-plugin:2.0.5.RELEASE")
    }
}

apply plugin: 'java'
apply plugin: 'org.springframework.boot'
apply plugin: 'io.spring.dependency-management'

bootJar {
    baseName = 'clicker'
    version =  '0.1.0-SNAPSHOT'
}

repositories {
    mavenCentral()
}

sourceCompatibility = 1.8
targetCompatibility = 1.8

dependencies {
    compile("org.springframework.boot:spring-boot-starter-web")
    testCompile('org.springframework.boot:spring-boot-starter-test')
}
```

## Application

The main entry point of a Spring Boot is a class annotated with `@SpringBootApplication`. The `@SpringBootApplication` annotation triggers the classpath scanning process that finds all classes marked as a controller (class that handles requests).

```java
package co.uk.minibuilds;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

## Controller

Controllers are Spring Boot componenents that handle HTTP requests, the `@RestController` annotation is used indicates that is a class is a controller allowing `@SpringBootApplication` find and use the class.
 

[`@GetMapping("/somepath")`](https://docs.spring.io/spring/docs/current/javadoc-api/org/springframework/web/bind/annotation/GetMapping.html) indicates that the annotated method should be used to handle GET requests to path "/somepath". Similarly `@PostMapping` handles POST requests, `@DeleteMapping` for DELETE requests, etc. The objects returned by these methods are automatically serialised to an HTTP response in JSON format (format can be configured using the produces argument in the mapping annotation)

```java
package co.uk.minibuilds;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.concurrent.atomic.AtomicLong;

@RestController
public class ClickerController {

    private final AtomicLong clickCount = new AtomicLong();

    @GetMapping("/click")
    public Click clickCount() {
        return new Click(clickCount.get());
    }

    @PostMapping("/click")
    Click click() {
        return new Click(clickCount.incrementAndGet());
    }

    public static class Click {
        private final long clickCount;

        public Click(long clickCount) {
            this.clickCount = clickCount;
        }

        public long getClickCount() {
            return clickCount;
        }
    }
}
```

## Static Content

Spring Boot serves files in the directory `resources/static`. For the clicker application we have added `index.html` which sends requests to the back end. 

## Build and Run

The Spring Boot Gradle plugin provides the `bootRun` task which is used to run Spring Boot applications.

```
gradlew bootRun
```

After running `gradlew bootRun` the Spring Boot application will be accessable at http://localhost:8080.

The usual `gradlew build` task can be used to build an uber jar. Gradle will put the jar in the directory `build/libs`, this jar can be run using `java -jar build/libs/clicker-0.1.0-SNAPSHOT.jar` 

## Docker

Just for fun lets wrap this application in a Docker container and run it. Below is a Dockerfile that will create a image that will have the Java runtime setup, contain the Spring Boot clicker jar, and run it on start up.

```
FROM openjdk:8-jdk-alpine
ADD build/libs/clicker-0.1.0-SNAPSHOT.jar /
ENTRYPOINT ["java", "-jar", "/clicker-0.1.0-SNAPSHOT.jar"]
```

With the Dockerfile in a directory called docker and the project built using `gradlew build` running `docker build` will create an image called clicker.

```
docker build -t clicker -f docker/Dockerfile .
```

`docker run` is used to run the clicker image. The `-p` argument is used to map the port 8080 from inside the container to outside. 

```
docker run -p 8080:8080 clicker
```

Navigating to http://localhost:8080 should show the same page as before when calling `gradlew bootRun`.