import java.util.List;
import java.util.ArrayList;
class Solution {
    public static int solution(int[] l) {
		// Each one of these is a second number to of one of the "lucky triples" (ie. y shown below)
		// A "lucky triple" is a tuple (x, y, z) where x divides y and y divides z, such as (1, 2, 4).
		List<Integer> secondNumbers = new ArrayList<Integer>();

		int tripleCount = 0;
		for (int i = 0; i < l.length; i++) {
			// Order matters here, check for triples before possibly adding this number to the secondNumbers list,
			// as that would result in false triples. (because we would see the second number is divisible by itself, the current number)
			for (int j = 0; j < secondNumbers.size(); j++) {
				if (l[i] % secondNumbers.get(j) == 0) {
					// Match! This is a lucky triple with the following form:
					//	( <unknown>, secondNumbers.get(j), l[i] )
					// <unknown> is guaranteed to fit the triple because it matches with the second number
					// and by definition has no relation to the third number in the triple.
					tripleCount++;
				}
			}

			for (int j = 0; j <= i-1; j++) {
				if (l[i] % l[j] == 0) {
					// Partial match! This could be a triple if <unknown> fits:
					//	( l[j], l[i], <unknown> )
					// To continue this Triple, we only need to know l[i] because the first number by
					// definition does not have any relation to the third number.
					secondNumbers.add(l[i]);
				}
			}
		}

		return tripleCount;
	}
}
