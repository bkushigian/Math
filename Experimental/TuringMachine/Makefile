CC=gcc
CFLAGS=-g -c
DEPS=
OBJS=obj/tm.o obj/hash.o
OBJDIR=obj
TESTDIR=test
BINDIR=bin

all: 

%: $(OBJDIR)/%.o
	$(CC) $(CFLAGS)  $< -o $(BINDIR)/$@

$(OBJDIR)/%.o: %.c
	$(CC) $(CFLAGS) -o $@ $<

$(TESTDIR)/%.o: $(TESTDIR)/%.c
	$(CC) $(CFLAGS) -c -o $@ $<

test_hash: $(TESTDIR)/test_hash.o $(OBJS)
	$(CC) -g $(TESTDIR)/test_hash.o $(OBJS) -o $(BINDIR)/test_hash

clean: 
	rm $(OBJDIR)/*.o  $(BINDIR)/* $(TESTDIR)/*.o

tests: test_hash

