# Design Parking

## System Requirements

1. The parking lot should have multiple floors where customers can park their cars.
2. The parking lot should have multiple entry and exit points.
3. Customers can collect a parking ticket from the entry points and can pay the parking fee at the exit points on their way out.
4. Customers can pay the tickets at the automated exit panel or to the parking attendant.
5. Customers can pay via both cash and credit cards.
6. Customers should also be able to pay the parking fee at the customer’s info portal on each floor. If the customer has paid at the info portal, they don’t have to pay at the exit.
7. The system should not allow more vehicles than the maximum capacity of the parking lot. If the parking is full, the system should be able to show a message at the entrance panel and on the parking display board on the ground floor.
8. Each parking floor will have many parking spots. The system should support multiple types of parking spots such as Compact, Large, Handicapped, Motorcycle, etc.
9. The Parking lot should have some parking spots specified for electric cars. These spots should have an electric panel through which customers can pay and charge their vehicles.
10. The system should support parking for different types of vehicles like car, truck, van, motorcycle, etc.
11. Each parking floor should have a display board showing any free parking spot for each spot type.
12. The system should support a per-hour parking fee model. For example, customers have to pay $4 for the first hour, $3.5 for the second and third hours, and $2.5 for all the remaining hours.

## Use Case Diagram

### Actors

* **Admin:** Mainly responsible for adding and modifying parking floors, parking spots, entrance, and exit panels, adding/removing parking attendants, etc.
* **Customer:** All customers can get a parking ticket and pay for it.
* **Parking Attendant:** Parking attendants can do all the activities on the customer’s behalf, and can take cash for ticket payment.
* **System:** To display messages on different info panels, as well as assigning and removing a vehicle from a parking spot.

### Actions

* **Add/Remove/Edit parking floor:** To add, remove or modify a parking floor from the system. Each floor can have its own display board to show free parking spots.
* **Add/Remove/Edit parking spot:** To add, remove or modify a parking spot on a parking floor.
* **Add/Remove a parking attendant:** To add or remove a parking attendant from the system.
* **Take ticket:** To provide customers with a new parking ticket when entering the parking lot.
* **Scan ticket:** To scan a ticket to find out the total charge.
* **Credit card payment:** To pay the ticket fee with credit card.
* **Cash payment:** To pay the parking ticket through cash.
* **Add/Modify parking rate:** To allow admin to add or modify the hourly parking rate.

<img src="../.gitbook/assets/file.excalidraw (1).svg" alt="" class="gitbook-drawing">

## Class Diagram

* **ParkingLot:** The central part of the organization for which this software has been designed. It has attributes like ‘Name’ to distinguish it from any other parking lots and ‘Address’ to define its location.
* **ParkingFloor:** The parking lot will have many parking floors.
* **ParkingSpot:** Each parking floor will have many parking spots. Our system will support different parking spots 1) Handicapped, 2) Compact, 3) Large, 4) Motorcycle, and 5) Electric.
* **Account:** We will have two types of accounts in the system: one for an Admin, and the other for a parking attendant.
* **Parking ticket:** This class will encapsulate a parking ticket. Customers will take a ticket when they enter the parking lot.
* **Vehicle:** Vehicles will be parked in the parking spots. Our system will support different types of vehicles 1) Car, 2) Truck, 3) Electric, 4) Van and 5) Motorcycle.
* **EntrancePanel and ExitPanel:** EntrancePanel will print tickets, and ExitPanel will facilitate payment of the ticket fee.
* **Payment:** This class will be responsible for making payments. The system will support credit card and cash transactions.
* **ParkingRate:** This class will keep track of the hourly parking rates. It will specify a dollar amount for each hour. For example, for a two hour parking ticket, this class will define the cost for the first and the second hour.
* **ParkingDisplayBoard:** Each parking floor will have a display board to show available parking spots for each spot type. This class will be responsible for displaying the latest availability of free parking spots to the customers.
* **ParkingAttendantPortal:** This class will encapsulate all the operations that an attendant can perform, like scanning tickets and processing payments.
* **CustomerInfoPortal:** This class will encapsulate the info portal that customers use to pay for the parking ticket. Once paid, the info portal will update the ticket to keep track of the payment.
* **ElectricPanel:** Customers will use the electric panels to pay and charge their electric vehicles.

```cpp
enum class VehicleType {
    CAR = 1,
    TRUCK = 2,
    ELECTRIC = 3,
    VAN = 4,
    MOTORBIKE = 5
};

enum class ParkingSpotType {
    HANDICAPPED = 1,
    COMPACT = 2,
    LARGE = 3,
    MOTORBIKE = 4,
    ELECTRIC = 5
};

enum class AccountStatus {
    ACTIVE = 1,
    BLOCKED = 2,
    BANNED = 3,
    COMPROMISED = 4,
    ARCHIVED = 5,
    UNKNOWN = 6
};

enum class ParkingTicketStatus {
    ACTIVE = 1,
    PAID = 2,
    LOST = 3
};

class Address {
public:
    Address(std::string street, std::string city, std::string state, std::string zip_code, std::string country)
        : street_address(street), city(city), state(state), zip_code(zip_code), country(country) {}

private:
    std::string street_address;
    std::string city;
    std::string state;
    std::string zip_code;
    std::string country;
};

class Person {
public:
    Person(std::string name, Address address, std::string email, std::string phone)
        : name(name), address(address), email(email), phone(phone) {}

private:
    std::string name;
    Address address;
    std::string email;
    std::string phone;
};

class Account {
public:
    Account(std::string user_name, std::string password, Person person, AccountStatus status = AccountStatus::ACTIVE)
        : user_name(user_name), password(password), person(person), status(status) {}

    void reset_password() {
        // Implement password reset logic here
    }

private:
    std::string user_name;
    std::string password;
    Person person;
    AccountStatus status;
};

class Admin : public Account {
public:
    Admin(std::string user_name, std::string password, Person person, AccountStatus status = AccountStatus::ACTIVE)
        : Account(user_name, password, person, status) {}

    void add_parking_floor(std::string floor) {
        // Implement adding a parking floor logic here
    }

    void add_parking_spot(std::string floor_name, std::string spot) {
        // Implement adding a parking spot logic here
    }

    void add_parking_display_board(std::string floor_name, std::string display_board) {
        // Implement adding a parking display board logic here
    }

    void add_customer_info_panel(std::string floor_name, std::string info_panel) {
        // Implement adding a customer info panel logic here
    }

    void add_entrance_panel(std::string entrance_panel) {
        // Implement adding an entrance panel logic here
    }

    void add_exit_panel(std::string exit_panel) {
        // Implement adding an exit panel logic here
    }
};

class ParkingAttendant : public Account {
public:
    ParkingAttendant(std::string user_name, std::string password, Person person, AccountStatus status = AccountStatus::ACTIVE)
        : Account(user_name, password, person, status) {}

    void process_ticket(std::string ticket_number) {
        // Implement processing a parking ticket logic here
    }
};

class ParkingSpot {
public:
    ParkingSpot(int number, ParkingSpotType parking_spot_type)
        : number(number), free(true), vehicle(nullptr), parking_spot_type(parking_spot_type) {}

    bool is_free() const {
        return free;
    }

    void assign_vehicle(std::string vehicle) {
        this->vehicle = vehicle;
        free = false;
    }

    void remove_vehicle() {
        vehicle = "";
        free = true;
    }

private:
    int number;
    bool free;
    std::string vehicle;
    ParkingSpotType parking_spot_type;
};

class HandicappedSpot : public ParkingSpot {
public:
    HandicappedSpot(int number) : ParkingSpot(number, ParkingSpotType::HANDICAPPED) {}
};

class CompactSpot : public ParkingSpot {
public:
    CompactSpot(int number) : ParkingSpot(number, ParkingSpotType::COMPACT) {}
};

class LargeSpot : public ParkingSpot {
public:
    LargeSpot(int number) : ParkingSpot(number, ParkingSpotType::LARGE) {}
};

class MotorbikeSpot : public ParkingSpot {
public:
    MotorbikeSpot(int number) : ParkingSpot(number, ParkingSpotType::MOTORBIKE) {}
};

class ElectricSpot : public ParkingSpot {
public:
    ElectricSpot(int number) : ParkingSpot(number, ParkingSpotType::ELECTRIC) {}
};

class ParkingFloor {
public:
    ParkingFloor(std::string name)
        : name(name), display_board(ParkingDisplayBoard()) {}

    void add_parking_spot(ParkingSpot spot) {
        switch (spot.get_type()) {
            case ParkingSpotType::HANDICAPPED:
                handicapped_spots[spot.get_number()] = spot;
                break;
            case ParkingSpotType::COMPACT:
                compact_spots[spot.get_number()] = spot;
                break;
            case ParkingSpotType::LARGE:
                large_spots[spot.get_number()] = spot;
                break;
            case ParkingSpotType::MOTORBIKE:
                motorbike_spots[spot.get_number()] = spot;
                break;
            case ParkingSpotType::ELECTRIC:
                electric_spots[spot.get_number()] = spot;
                break;
            default:
                std::cout << "Wrong parking spot type!" << std::endl;
        }
    }

    void assign_vehicle_to_spot(std::string vehicle, ParkingSpot spot) {
        spot.assign_vehicle(vehicle);
        switch (spot.get_type()) {
            case ParkingSpotType::HANDICAPPED:
                update_display_board_for_handicapped(spot);
                break;
            case ParkingSpotType::COMPACT:
                update_display_board_for_compact(spot);
                break;
            case ParkingSpotType::LARGE:
                update_display_board_for_large(spot);
                break;
            case ParkingSpotType::MOTORBIKE:
                update_display_board_for_motorbike(spot);
                break;
            case ParkingSpotType::ELECTRIC:
                update_display_board_for_electric(spot);
                break;
            default:
                std::cout << "Wrong parking spot type!" << std::endl;
        }
    }

    void update_display_board_for_handicapped(ParkingSpot spot) {
        if (display_board.get_handicapped_free_spot().get_number() == spot.get_number()) {
            // Find another free handicapped parking and assign it to the display_board
            for (const auto& entry : handicapped_spots) {
                if (entry.second.is_free()) {
                    display_board.set_handicapped_free_spot(entry.second);
                    break;
                }
            }
            display_board.show_empty_spot_number();
        }
    }

    void update_display_board_for_compact(ParkingSpot spot) {
        if (display_board.get_compact_free_spot().get_number() == spot.get_number()) {
            // Find another free compact parking and assign it to the display_board
            for (const auto& entry : compact_spots) {
                if (entry.second.is_free()) {
                    display_board.set_compact_free_spot(entry.second);
                    break;
                }
            }
            display_board.show_empty_spot_number();
        }
    }

    void free_spot(ParkingSpot spot) {
        spot.remove_vehicle();
        switch (spot.get_type()) {
            case ParkingSpotType::HANDICAPPED:
                free_handicapped_spot_count["free_spot"]++;
                break;
            case ParkingSpotType::COMPACT:
                free_compact_spot_count["free_spot"]++;
                break;
            case ParkingSpotType::LARGE:
                free_large_spot_count["free_spot"]++;
                break;
            case ParkingSpotType::MOTORBIKE:
                free_motorbike_spot_count["free_spot"]++;
                break;
            case ParkingSpotType::ELECTRIC:
                free_electric_spot_count["free_spot"]++;
                break;
            default:
                std::cout << "Wrong parking spot type!" << std::endl;
        }
    }
    
private:
    std::string name;
    std::map<int, ParkingSpot> handicapped_spots;
    std::map<int, ParkingSpot> compact_spots;
    std::map<int, ParkingSpot> large_spots;
    std::map<int, ParkingSpot> motorbike_spots;
    std::map<int, ParkingSpot> electric_spots;
    std::map<std::string, int> free_handicapped_spot_count = {{"free_spot", 0}};
    std::map<std::string, int> free_compact_spot_count = {{"free_spot", 0}};
    std::map<std::string, int> free_large_spot_count = {{"free_spot", 0}};
    std::map<std::string, int> free_motorbike_spot_count = {{"free_spot", 0}};
    std::map<std::string, int> free_electric_spot_count = {{"free_spot", 0}};
    ParkingDisplayBoard display_board;
};

class ParkingDisplayBoard {
public:
    ParkingDisplayBoard(std::string id)
        : id(id), handicapped_free_spot(nullptr), compact_free_spot(nullptr),
          large_free_spot(nullptr), motorbike_free_spot(nullptr), electric_free_spot(nullptr) {}

    void show_empty_spot_number() {
        std::string message = "";

        if (handicapped_free_spot != nullptr && handicapped_free_spot->is_free()) {
            message += "Free Handicapped: " + std::to_string(handicapped_free_spot->get_number());
        } else {
            message += "Handicapped is full";
        }
        message += "\n";

        if (compact_free_spot != nullptr && compact_free_spot->is_free()) {
            message += "Free Compact: " + std::to_string(compact_free_spot->get_number());
        } else {
            message += "Compact is full";
        }
        message += "\n";

        if (large_free_spot != nullptr && large_free_spot->is_free()) {
            message += "Free Large: " + std::to_string(large_free_spot->get_number());
        } else {
            message += "Large is full";
        }
        message += "\n";

        if (motorbike_free_spot != nullptr && motorbike_free_spot->is_free()) {
            message += "Free Motorbike: " + std::to_string(motorbike_free_spot->get_number());
        } else {
            message += "Motorbike is full";
        }
        message += "\n";

        if (electric_free_spot != nullptr && electric_free_spot->is_free()) {
            message += "Free Electric: " + std::to_string(electric_free_spot->get_number());
        } else {
            message += "Electric is full";
        }

        std::cout << message << std::endl;
    }

    void set_handicapped_free_spot(ParkingSpot* spot) {
        handicapped_free_spot = spot;
    }

    void set_compact_free_spot(ParkingSpot* spot) {
        compact_free_spot = spot;
    }

    void set_large_free_spot(ParkingSpot* spot) {
        large_free_spot = spot;
    }

    void set_motorbike_free_spot(ParkingSpot* spot) {
        motorbike_free_spot = spot;
    }

    void set_electric_free_spot(ParkingSpot* spot) {
        electric_free_spot = spot;
    }

private:
    std::string id;
    ParkingSpot* handicapped_free_spot;
    ParkingSpot* compact_free_spot;
    ParkingSpot* large_free_spot;
    ParkingSpot* motorbike_free_spot;
    ParkingSpot* electric_free_spot;
};

class ParkingTicket;

class ParkingLot {
private:
    static ParkingLot* instance;

    class OnlyOne {
    public:
        OnlyOne(const std::string& name, const std::string& address) :
            name(name), address(address), parking_rate(0.0), max_compact_count(0), max_large_count(0),
            max_motorbike_count(0), max_electric_count(0) {}

        std::string name;
        std::string address;
        double parking_rate;
        int compact_spot_count;
        int large_spot_count;
        int motorbike_spot_count;
        int electric_spot_count;
        int max_compact_count;
        int max_large_count;
        int max_motorbike_count;
        int max_electric_count;

        std::map<std::string, int> free_handicapped_spot_count;
        std::map<std::string, int> free_compact_spot_count;
        std::map<std::string, int> free_large_spot_count;
        std::map<std::string, int> free_motorbike_spot_count;
        std::map<std::string, int> free_electric_spot_count;

        std::map<std::string, std::string> entrance_panels;
        std::map<std::string, std::string> exit_panels;

        std::map<std::string, ParkingTicket> active_tickets;
        std::mutex lock;
    };

    OnlyOne* parking_lot;

public:
    static ParkingLot* get_instance(const std::string& name, const std::string& address) {
        if (!instance) {
            instance = new ParkingLot(name, address);
        }
        return instance;
    }

    ParkingTicket get_new_parking_ticket(const Vehicle& vehicle) {
        if (is_full(vehicle.get_type())) {
            throw std::runtime_error("Parking full!");
        }

        parking_lot->lock.lock();
        ParkingTicket ticket;
        vehicle.assign_ticket(ticket);
        ticket.save_in_DB(); // Implement this method for database interaction.
        increment_spot_count(vehicle.get_type());
        parking_lot->active_tickets[ticket.get_ticket_number()] = ticket;
        parking_lot->lock.unlock();

        return ticket;
    }

    bool is_full(VehicleType type) {
        if (type == VehicleType::Truck || type == VehicleType::Van) {
            return parking_lot->large_spot_count >= parking_lot->max_large_count;
        }
        else if (type == VehicleType::Motorbike) {
            return parking_lot->motorbike_spot_count >= parking_lot->max_motorbike_count;
        }
        else if (type == VehicleType::Car) {
            return (parking_lot->compact_spot_count + parking_lot->large_spot_count) >=
                (parking_lot->max_compact_count + parking_lot->max_large_count);
        }
        else { // Electric car
            return (parking_lot->compact_spot_count + parking_lot->large_spot_count +
                parking_lot->electric_spot_count) >=
                (parking_lot->max_compact_count + parking_lot->max_large_count +
                    parking_lot->max_electric_count);
        }
    }

    void increment_spot_count(VehicleType type) {
        if (type == VehicleType::Truck || type == VehicleType::Van) {
            parking_lot->large_spot_count++;
        }
        else if (type == VehicleType::Motorbike) {
            parking_lot->motorbike_spot_count++;
        }
        else if (type == VehicleType::Car) {
            if (parking_lot->compact_spot_count < parking_lot->max_compact_count) {
                parking_lot->compact_spot_count++;
            }
            else {
                parking_lot->large_spot_count++;
            }
        }
        else { // Electric car
            if (parking_lot->electric_spot_count < parking_lot->max_electric_count) {
                parking_lot->electric_spot_count++;
            }
            else if (parking_lot->compact_spot_count < parking_lot->max_compact_count) {
                parking_lot->compact_spot_count++;
            }
            else {
                parking_lot->large_spot_count++;
            }
        }
    }

    // Implement other methods (add_parking_floor, add_entrance_panel, add_exit_panel) similarly.
};

ParkingLot* ParkingLot::instance = nullptr;
```
