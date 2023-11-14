-- Keep a log of any SQL queries you execute as you solve the mystery.
--SELECT description FROM crime_scene_reports WHERE month = 7 AND day = 28 AND street = "Humphrey Street"
-- Answer was:
--Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.
--Littering took place at 16:36. No known witnesses.
------------------------------------------------------------------------------------------------------------------------------------------------------
--SELECT transcript FROM interviews WHERE month = 7 AND day = 28;
-- Answer was:                                                                                                                |
-- Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.                                                          |
-- I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.                                                                                                 |
-- As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket. |
------------------------------------------------------------------------------------------------------------------------------------------------------
--SELECT account_number FROM atm_transactions WHERE month = 7 AND day = 28 AND atm_location = "Leggett Street";
-- Answers:
--+----------------+
--| account_number |
--+----------------+
--| 28500762       |
--| 28296815       |
--| 76054385       |
--| 49610011       |
--| 16153065       |
--| 86363979       |
--| 25506511       |
--| 81061156       |
--| 26013199       |
--+----------------+
----------------------------------------------------------------------------------------------------------------------------------------------------
--SELECT origin_airport_id, destination_airport_id, hour, minute, id FROM flights WHERE month = 7 AND day = 29 ORDER BY hour LIMIT 1;
-- Answers:
--+-------------------+------------------------+------+--------+
--| origin_airport_id | destination_airport_id | hour | minute |
--+-------------------+------------------------+------+--------+
--| 8                 | 6                      | 16   | 0      |
--| 8                 | 11                     | 12   | 15     |
--| 8                 | 4                      | 8    | 20     |
--| 8                 | 1                      | 9    | 30     |
--| 8                 | 9                      | 15   | 20     |
--+-------------------+------------------------+------+--------+
---------------------------------------------------------------------------------------------------------------------------------------------------
SELECT name FROM people
    JOIN passengers ON people.passport_number = passengers.passport_number
    JOIN flights ON passengers.flight_id = flights.id
    WHERE flights.id = (
        SELECT id FROM flights
            WHERE month = 7
            AND day = 29
            ORDER BY hour LIMIT 1
            )
    AND people.id = (
        SELECT people.id FROM people
        JOIN bank_accounts ON people.id = bank_accounts.person_id
        JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
        WHERE month = 7
        AND day = 28
        AND atm_location = "Leggett Street"
    );

SELECT city FROM airports
    JOIN flights ON airports.id = flights.destination_airport_id
    WHERE flights.id = (
        SELECT id FROM flights
            WHERE month = 7
            AND day = 29
            ORDER BY hour LIMIT 1
    );

SELECT name FROM people
    WHERE people.phone_number = (
        SELECT people.phone_number FROM people
            JOIN phone_calls ON people.phone_number = phone_calls.receiver
            WHERE month = 7
            AND day = 28
            AND phone_calls.caller = (
                SELECT people.phone_number FROM people
                JOIN phone_calls ON people.phone_number = phone_calls.caller
                WHERE name = (
                    SELECT name FROM people
    JOIN passengers ON people.passport_number = passengers.passport_number
    JOIN flights ON passengers.flight_id = flights.id
    WHERE flights.id = (
        SELECT id FROM flights
            WHERE month = 7
            AND day = 29
            ORDER BY hour LIMIT 1
            )
    AND people.id = (
        SELECT people.id FROM people
        JOIN bank_accounts ON people.id = bank_accounts.person_id
        JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
        WHERE month = 7
        AND day = 28
        AND atm_location = "Leggett Street"
    )
                )
            )
    );

SELECT name FROM people
    JOIN phone_calls ON people.phone_number = phone_calls.receiver
    WHERE month = 7
    AND day = 28
    AND duration < 60;