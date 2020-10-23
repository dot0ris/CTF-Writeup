#include <iostream>
#include <sstream>
#include <vector>
#include <string>
#include <map>
#include <limits>
#include <cstdlib>
#include <unistd.h>
#include <signal.h>
#include <execinfo.h>
#include "movement.hpp"
#include "util.hpp"

#define ALARM_SECONDS 30


std::map<std::string, Movement*> mm;

void init();
void print_intro();
int menu();
void compose();
void revise();
void review();
void execute();
static void handle_sigalrm(int);
static void print_backtrace();

int main(void)
{
    init();
    print_intro();
    for (;;)
    {
        switch (menu())
        {
            case 1: {
                compose();
            } break;
            case 2: {
                revise();
            } break;
            case 3: {
                review();
            } break;
            case 4: {
                execute();
            } break;
            default: {
                exit(0);
            } break;
        }
    }
}

void init()
{
    // C++-style unbuffered
    std::cin.setf(std::ios::unitbuf);
    std::cout.setf(std::ios::unitbuf);
    std::cerr.setf(std::ios::unitbuf);

    // C-style unbuffered
    if (setvbuf(stdin, NULL, _IONBF, 0) ||
        setvbuf(stdout, NULL, _IONBF, 0) ||
        setvbuf(stderr, NULL, _IONBF, 0))
        exit(1);

    // unset LD_PRELOAD for everyone's mental tranquility
    if (unsetenv("LD_PRELOAD"))
        exit(1);

    signal(SIGALRM, handle_sigalrm);
    alarm(ALARM_SECONDS);
}

static void handle_sigalrm(int sig __attribute__((unused)))
{
    exit(0);
}

void print_intro()
{
    std::cout << "Choreographer v0.1" << std::endl;
}

int menu()
{
    std::cout << "1. Compose" << std::endl;
    std::cout << "2. Revise" << std::endl;
    std::cout << "3. Review" << std::endl;
    std::cout << "4. Execute" << std::endl;
    std::cout << "5. Exit" << std::endl;
    std::cout << "> ";

    int sel;
    std::cin >> sel;

    if (std::cin.good())
        return sel;
    return 5;
}

void compose()
{
    std::cout << "<Composition Mode>" << std::endl;

    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    for (;;)
    {
        std::string line, name, type;
        std::stringstream input;

        std::cout << "> ";
        std::getline(std::cin, line);
        if (!std::cin.good())
            break;
        
        input.str(line);

        input >> name;
        if (name == ":q")
            break;
        else if (!isid(name))
        {
            std::cout << "Invalid movement name." << std::endl;
            continue;
        }
        else if (mm.find(name) != mm.end())
        {
            std::cout << "Movement name already present." << std::endl;
            continue;
        }

        input >> type;
        if (type == "basic")
        {
            std::string res;
            if (!getUnescString(input, res))
            {
                std::cout << "Invalid basic movement description." << std::endl;
                continue;
            }
            mm[name] = new BaseMove(name, res);
        }
        else if (type == "rep")
        {
            std::string rep_name;
            input >> rep_name;
            auto rep_mv_iter = mm.find(rep_name);
            if (rep_mv_iter == mm.end())
            {
                std::cout << "Movement not present." << std::endl;
                continue;
            }
            Movement *rep_mv = (*rep_mv_iter).second;

            int repeat;
            input >> repeat;
            if (repeat <= 0 || repeat > 0x10)
            {
                std::cout << "Invalid repetition movement count." << std::endl;
                continue;
            }
            mm[name] = new RepetitionMove(name, rep_mv, repeat);
        }
        else if (type == "seq" || type == "acc")
        {
            bool isSeq = type == "seq";
            int cnt;
            input >> cnt;
            if (cnt <= 0 || cnt > 0x10)
            {
                std::cout << "Invalid " << (isSeq ? "sequence" : "accumulation") << " movement count." << std::endl;
                continue;
            }

            std::vector<Movement*> mvs;
            for (int i = 0; i < cnt; i++)
            {
                std::string mv_name;
                input >> mv_name;
                auto mv_iter = mm.find(mv_name);
                if (mv_iter == mm.end())
                {
                    std::cout << "Movement not present." << std::endl;
                    break;
                }
                mvs.push_back((*mv_iter).second);
            }
            if ((signed)mvs.size() != cnt)  // break
                continue;
            
            if (isSeq)
                mm[name] = new SequenceMove(name, mvs);
            else
                mm[name] = new AccumulationMove(name, mvs);
        }
        else if (type == "rev" || type == "ret")
        {
            std::string mv_name;
            input >> mv_name;
            auto mv_iter = mm.find(mv_name);
            if (mv_iter == mm.end())
            {
                std::cout << "Movement not present." << std::endl;
                continue;
            }
            Movement *mv = (*mv_iter).second;

            if (type == "rev")
                mm[name] = new ReversalMove(name, mv);
            else
                mm[name] = new RetrogradeMove(name, mv);
        }
        else
        {
            std::cout << "Invalid movement type." << std::endl;
            continue;
        }
    }
}

void revise()
{
    std::cout << "<Revision Mode>" << std::endl;

    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    for (;;)
    {
        std::string line, name;
        std::stringstream input;

        std::cout << "> ";
        std::getline(std::cin, line);
        if (!std::cin.good())
            break;
        
        input.str(line);

        input >> name;
        if (!std::cin.good() || name == ":q")
            break;

        auto mv_iter = mm.find(name);
        if (mv_iter == mm.end())
        {
            std::cout << "Movement not present." << std::endl;
            continue;
        }

        int revision_at;
        input >> revision_at;
        if (revision_at < 0)
        {
            std::cout << "Invalid revision index." << std::endl;
            continue;
        }

        std::string revise_to;
        if (!getUnescString(input, revise_to))
        {
            std::cout << "Invalid revision description." << std::endl;
            continue;
        }

        mm[name] = new RevisedMove((*mv_iter).second, revision_at, revise_to);
    }
}

void review()
{
    std::cout << "<Review Mode>" << std::endl;

    for (;;)
    {
        std::cout << "> ";

        std::string name;
        std::cin >> name;
        if (!std::cin.good() || name == ":q")
            break;

        auto mv_iter = mm.find(name);
        if (mv_iter == mm.end())
        {
            std::cout << "Movement not present." << std::endl;
            continue;
        }

        std::cout << "[Movement " << name << "]" << std::endl;
        std::cout << (*mv_iter).second->getRepr() << std::endl;
    }
}

void execute()
{
    std::cout << "<Execution Mode>" << std::endl;

    for (;;)
    {
        std::cout << "> ";
        
        std::string name;
        std::cin >> name;
        if (!std::cin.good() || name == ":q")
            break;

        auto mv_iter = mm.find(name);
        if (mv_iter == mm.end())
        {
            std::cout << "Movement not present." << std::endl;
            continue;
        }

        std::function<std::string(std::string const&)> f = [](std::string const &s){ return s; };

        try
        {
            std::cout << "[Movement " << name << "]" << std::endl;
            std::cout << join("\n", (*mv_iter).second->getStr(), f) << std::endl;
        }
        catch (...)
        {
            std::cout << "Something went wrong." << std::endl;
            std::cout << "Crash Log:" << std::endl;
            print_backtrace();
            std::cout << "Attempting crash recovery..." << std::endl;
            break;
        }
    }
}

static void print_backtrace()
{
    void *array[10];
    size_t size;

    // get void*'s for all entries on the stack
    size = backtrace(array, 10);

    // print out all the frames to stderr
    backtrace_symbols_fd(array, size, STDOUT_FILENO);
}