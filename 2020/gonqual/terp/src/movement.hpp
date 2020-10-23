#pragma once

#include <map>
#include <string>
#include <sstream>
#include <vector>
#include <functional>

class Movement
{
public:
    Movement(const std::string &name): name(name) {}
    virtual std::string getRepr() const = 0;
    virtual std::vector<std::string> getStr() const = 0;
    virtual bool contains(const Movement * m) const = 0;
    static std::function<std::string(Movement* const&)> getReprFunc;
    const std::string &getName() const
    {
        return name;
    }

private:
    std::string name;
};

// base move only having string description
class BaseMove: public Movement
{
public:
    BaseMove(std::string &name, std::string &desc):
        Movement(name), desc(desc) {}
    std::string getRepr() const override;
    std::vector<std::string> getStr() const override;
    bool contains(const Movement * m) const override;

private:
    std::string desc;
};

// repeat move for N times
class RepetitionMove: public Movement
{
public:
    RepetitionMove(std::string &name, Movement *mv, int repeat):
        Movement(name), mv(mv), repeat(repeat) {}
    std::string getRepr() const override;
    std::vector<std::string> getStr() const override;
    bool contains(const Movement * m) const override;

private:
    Movement *mv;
    int repeat;
};

// sequence of moves
class SequenceMove: public Movement
{
public:
    SequenceMove(std::string &name, const std::vector<Movement*> &mvs):
        Movement(name), mvs(mvs) {}
    std::string getRepr() const override;
    std::vector<std::string> getStr() const override;
    bool contains(const Movement * m) const override;

private:
    std::vector<Movement*> mvs;
};

// A -> AB -> ABC -> ABCD style move
class AccumulationMove: public Movement
{
public:
    AccumulationMove(std::string &name, std::vector<Movement*> &mvs):
        Movement(name), mvs(mvs) {}
    std::string getRepr() const override;
    std::vector<std::string> getStr() const override;
    bool contains(const Movement * m) const override;

private:
    std::vector<Movement*> mvs;
};

// move order reversed (shallow reversal)
class ReversalMove: public Movement
{
public:
    ReversalMove(std::string &name, Movement *mv):
        Movement(name), mv(mv) {}
    std::string getRepr() const override;
    std::vector<std::string> getStr() const override;
    bool contains(const Movement * m) const override;
    
private:
    Movement *mv;
};

// result of whole move themselve reversed (complete reversal)
class RetrogradeMove: public Movement
{
public:
    RetrogradeMove(std::string &name, Movement *mv):
        Movement(name), mv(mv) {}
    std::string getRepr() const override;
    std::vector<std::string> getStr() const override;
    bool contains(const Movement * m) const override;
    
private:
    Movement *mv;
};

// single index revision
class RevisedMove: public Movement
{
public:
    RevisedMove(Movement *base_mv, int revision_at, const std::string &revise_to):
        Movement(base_mv->getName()), base_mv(base_mv), revision_at(revision_at), revise_to(revise_to) {}
    std::string getRepr() const override;
    std::vector<std::string> getStr() const override;
    bool contains(const Movement * m) const override;
    
private:
    Movement *base_mv;
    int revision_at;
    std::string revise_to;
};