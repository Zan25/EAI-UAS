import request from "supertest";
import { expect } from "chai";

const app = "http://localhost:3000"; // URL of your server

// API key for authentication
const apiKey = "FINALPROJECTEAI";
const headers = { "x-api-key": apiKey };

describe("API Availability and Functionality Tests", () => {
  it("should return 200 OK for GET /flight", (done) => {
    request(app)
      .get("/flight")
      .set(headers)
      .expect(200)
      .end((err, res) => {
        if (err) return done(err);
        expect(res.body).to.have.property("success", true);
        done();
      });
  });

  it("should create a new flight ticket", (done) => {
    const newFlight = {
      airline: "Air Test",
      flight_number: "AT1234",
      departure_city: "City A",
      destination_city: "City B",
      departure_date: "2024-12-01",
      arrival_date: "2024-12-01",
      price: 100,
      departure_time: "10:00",
      arrival_time: "12:00",
    };

    request(app)
      .post("/flight")
      .set(headers)
      .send(newFlight)
      .expect(201)
      .end((err, res) => {
        if (err) return done(err);
        expect(res.body).to.have.property("success", true);
        done();
      });
  });

  // Add more tests for other endpoints similarly
  it("should return 200 OK for GET /train", (done) => {
    request(app)
      .get("/train")
      .set(headers)
      .expect(200)
      .end((err, res) => {
        if (err) return done(err);
        expect(res.body).to.have.property("success", true);
        done();
      });
  });

  it("should create a new train ticket", (done) => {
    const newTrain = {
      train_operator: "Train Test",
      train_number: "TT1234",
      departure_station: "Station A",
      destination_station: "Station B",
      departure_date: "2024-12-01",
      arrival_date: "2024-12-01",
      departure_time: "10:00",
      arrival_time: "12:00",
      price: 50,
    };

    request(app)
      .post("/train")
      .set(headers)
      .send(newTrain)
      .expect(201)
      .end((err, res) => {
        if (err) return done(err);
        expect(res.body).to.have.property("success", true);
        done();
      });
  });

  it("should return 200 OK for GET /hotel", (done) => {
    request(app)
      .get("/hotel")
      .set(headers)
      .expect(200)
      .end((err, res) => {
        if (err) return done(err);
        expect(res.body).to.have.property("success", true);
        done();
      });
  });

  it("should create a new hotel", (done) => {
    const newHotel = {
      hotel_name: "Hotel Test",
      location: "City Test",
      star_rating: 5,
      description: "Test description",
      price_per_night: 200,
      room_type: "Deluxe",
    };

    request(app)
      .post("/hotel")
      .set(headers)
      .send(newHotel)
      .expect(201)
      .end((err, res) => {
        if (err) return done(err);
        expect(res.body).to.have.property("success", true);
        done();
      });
  });

  it("should return 200 OK for GET /attractions", (done) => {
    request(app)
      .get("/attractions")
      .set(headers)
      .expect(200)
      .end((err, res) => {
        if (err) return done(err);
        expect(res.body).to.have.property("success", true);
        done();
      });
  });

  it("should create a new attraction", (done) => {
    const newAttraction = {
      attraction_name: "Attraction Test",
      location: "Location Test",
      description: "Test description",
      ticket_price: 20,
    };

    request(app)
      .post("/attractions")
      .set(headers)
      .send(newAttraction)
      .expect(201)
      .end((err, res) => {
        if (err) return done(err);
        expect(res.body).to.have.property("success", true);
        done();
      });
  });

  it("should create a new order", (done) => {
    const newOrder = {
      order_type: "flight",
      customer_name: "Customer Test",
      email: "customer@test.com",
      phone_number: "123456789",
    };

    request(app)
      .post("/order")
      .set(headers)
      .send(newOrder)
      .expect(200)
      .end((err, res) => {
        if (err) return done(err);
        expect(res.body).to.have.property("success", true);
        done();
      });
  });
});
