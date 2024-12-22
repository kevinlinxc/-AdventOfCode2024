

package main

import (
	"bufio"
	"fmt"
	"os"
	"runtime"
	"strconv"
	"sync"
)

type Result struct {
	bananas  int
	sequence []int
}

func getBananas(n int64, sequence []int) int {
	lastNum := int(n % 10)
	currentDiffSeq := make([]int, 0, 4)

	for i := 0; i < 2000; i++ {
		n = ((n * 64) ^ n) % 16777216
		n = ((n / 32) ^ n) % 16777216
		n = ((n * 2048) ^ n) % 16777216

		newNum := int(n % 10)
		diff := newNum - lastNum

		currentDiffSeq = append(currentDiffSeq, diff)
		if len(currentDiffSeq) > 4 {
			currentDiffSeq = currentDiffSeq[1:]
		}

		if len(currentDiffSeq) == 4 {
			match := true
			for i := 0; i < 4; i++ {
				if currentDiffSeq[i] != sequence[i] {
					match = false
					break
				}
			}
			if match {
				return newNum
			}
		}

		lastNum = newNum
	}
	return 0
}

func worker(jobs <-chan []int, results chan<- Result, numbers []int64, wg *sync.WaitGroup) {
	defer wg.Done()

	for sequence := range jobs {
		bananas := 0
		for _, num := range numbers {
			bananas += getBananas(num, sequence)
		}
		results <- Result{
			bananas:  bananas,
			sequence: sequence,
		}
	}
}

func main() {
	// Read input file
	file, err := os.Open("inputs/22.txt")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	var numbers []int64
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		num, err := strconv.ParseInt(scanner.Text(), 10, 64)
		if err != nil {
			panic(err)
		}
		numbers = append(numbers, num)
	}

	// Set up channels
	numWorkers := runtime.NumCPU()
	jobs := make(chan []int, numWorkers)
	results := make(chan Result, numWorkers)

	// Start workers
	var wg sync.WaitGroup
	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		go worker(jobs, results, numbers, &wg)
	}

	// Start result collector
	maxResult := Result{bananas: 0}
	done := make(chan bool)
	go func() {
		for result := range results {
			if result.bananas > maxResult.bananas {
				maxResult = result
				fmt.Printf("New max: %d with %v\n", result.bananas, result.sequence)
			}
		}
		done <- true
	}()

	// Generate all sequences
	for a := -10; a <= 10; a++ {
		for b := -10; b <= 10; b++ {
		//print b

			for c := -10; c <= 10; c++ {
				for d := -10; d <= 10; d++ {
					jobs <- []int{a, b, c, d}
				}
			}
		}
	}

	// Close channels and wait
	close(jobs)
	wg.Wait()
	close(results)
	<-done

	fmt.Println("Final maximum:", maxResult.bananas)
}
