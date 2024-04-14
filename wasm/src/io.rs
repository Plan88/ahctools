use modint::ModInt;
use proconio::{input, source::auto::AutoSource};
pub type Score = u64;

pub struct Input {
    pub n: usize,
    pub m: usize,
    pub k: usize,
    pub a: Vec<Vec<ModInt>>,
    pub s: Vec<Vec<Vec<ModInt>>>,
}

impl Input {
    pub fn parse_input(input_str: &str) -> Result<Self, String> {
        let source = AutoSource::from(input_str);
        input! {
            from source,
        (n, m, k): (usize, usize, usize),
        a_: [[u128; n]; n],
        s_: [[[u128; 3]; 3]; m],
        }

        let mut a = vec![vec![ModInt::new(0); n]; n];
        let mut s = vec![vec![vec![ModInt::new(0); 3]; 3]; m];

        for i in 0..n {
            for j in 0..n {
                a[i][j] = ModInt::new(a_[i][j]);
            }
        }
        for i in 0..m {
            for j in 0..3 {
                for k in 0..3 {
                    s[i][j][k] = ModInt::new(s_[i][j][k]);
                }
            }
        }

        Ok(Self { n, m, k, a, s })
    }
}

pub struct Output {
    l: usize,
    actions: Vec<(usize, usize, usize)>,
}

impl Output {
    pub fn parse_output(output_str: &str) -> Result<Self, String> {
        let source = AutoSource::from(output_str);
        input! {
            from source,
        l: usize,
        actions: [(usize, usize, usize); l],
        }

        Ok(Self { l, actions })
    }

    pub fn get_max_turn(&self, input: &Input) -> usize {
        self.l
    }

    pub fn get_state_at_turn(&self, input: &Input, turn: usize) -> Vec<Vec<u64>> {
        let mut a = input.a.clone();
        for &(i, x, y) in self.actions.iter().take(turn) {
            self.stamp(&mut a, &input.s[i], x, y);
        }

        let mut ret = vec![vec![0; input.n]; input.n];
        for i in 0..input.n {
            for j in 0..input.n {
                ret[i][j] = a[i][j].0 as u64;
            }
        }
        ret
    }

    fn stamp(&self, a: &mut Vec<Vec<ModInt>>, s: &Vec<Vec<ModInt>>, x: usize, y: usize) {
        for i in 0..3 {
            for j in 0..3 {
                a[x + i][y + j] += s[i][j];
            }
        }
    }

    pub fn calc_score(&self, input: &Input, turn: usize) -> Result<Score, String> {
        let a = self.get_state_at_turn(input, turn);
        let score = a
            .into_iter()
            .map(|v| v.into_iter().sum::<u64>())
            .into_iter()
            .sum();

        Ok(score)
    }
}

pub mod modint {
    use std::ops::{Add, AddAssign, Div, DivAssign, Mul, MulAssign, Sub, SubAssign};
    type Int = u128;

    #[derive(Clone, Copy)]
    pub struct ModInt(pub Int);

    impl ModInt {
        const MOD: Int = 998244353;

        pub fn new(x: Int) -> Self {
            Self(x % Self::MOD)
        }

        pub fn add(&self, other: Self) -> Self {
            let mut val = self.0 + other.0;
            if val >= Self::MOD {
                val -= Self::MOD;
            }
            Self(val)
        }

        pub fn sub(&self, other: Self) -> Self {
            let val = if self.0 >= other.0 {
                self.0 - other.0
            } else {
                Self::MOD - other.0 + self.0
            };
            Self(val)
        }

        pub fn mul(&self, other: Self) -> Self {
            Self((self.0 * other.0) % Self::MOD)
        }

        pub fn div(&self, other: Self) -> Self {
            self.mul(other.inv())
        }

        pub fn pow(&self, mut n: Int) -> Self {
            let mut val = 1;
            let mut pow = self.0;
            while n > 0 {
                if (n & 1) == 1 {
                    val = (val * pow) % Self::MOD;
                }
                pow = (pow * pow) % Self::MOD;
                n >>= 1;
            }
            Self(val)
        }

        pub fn inv(&self) -> Self {
            self.pow(Self::MOD - 2)
        }
    }

    impl Add for ModInt {
        type Output = ModInt;
        fn add(self, rhs: Self) -> Self::Output {
            ModInt::add(&self, rhs)
        }
    }

    impl Sub for ModInt {
        type Output = ModInt;
        fn sub(self, rhs: Self) -> Self::Output {
            ModInt::sub(&self, rhs)
        }
    }

    impl Mul for ModInt {
        type Output = ModInt;
        fn mul(self, rhs: Self) -> Self::Output {
            ModInt::mul(&self, rhs)
        }
    }

    impl Div for ModInt {
        type Output = ModInt;
        fn div(self, rhs: Self) -> Self::Output {
            ModInt::div(&self, rhs)
        }
    }

    impl Add<Int> for ModInt {
        type Output = ModInt;
        fn add(self, rhs: Int) -> Self::Output {
            ModInt::add(&self, Self::new(rhs))
        }
    }

    impl Sub<Int> for ModInt {
        type Output = ModInt;
        fn sub(self, rhs: Int) -> Self::Output {
            ModInt::sub(&self, Self::new(rhs))
        }
    }

    impl Mul<Int> for ModInt {
        type Output = ModInt;
        fn mul(self, rhs: Int) -> Self::Output {
            ModInt::mul(&self, Self::new(rhs))
        }
    }

    impl Div<Int> for ModInt {
        type Output = ModInt;
        fn div(self, rhs: Int) -> Self::Output {
            ModInt::div(&self, Self::new(rhs))
        }
    }

    impl AddAssign<ModInt> for ModInt {
        fn add_assign(&mut self, rhs: ModInt) {
            *self = self.add(rhs);
        }
    }

    impl SubAssign<ModInt> for ModInt {
        fn sub_assign(&mut self, rhs: ModInt) {
            *self = self.sub(rhs);
        }
    }

    impl MulAssign<ModInt> for ModInt {
        fn mul_assign(&mut self, rhs: ModInt) {
            *self = self.mul(rhs);
        }
    }

    impl DivAssign<ModInt> for ModInt {
        fn div_assign(&mut self, rhs: ModInt) {
            *self = self.div(rhs);
        }
    }

    impl AddAssign<Int> for ModInt {
        fn add_assign(&mut self, rhs: Int) {
            *self = self.add(rhs);
        }
    }

    impl SubAssign<Int> for ModInt {
        fn sub_assign(&mut self, rhs: Int) {
            *self = self.sub(rhs);
        }
    }

    impl MulAssign<Int> for ModInt {
        fn mul_assign(&mut self, rhs: Int) {
            *self = self.mul(rhs);
        }
    }

    impl DivAssign<Int> for ModInt {
        fn div_assign(&mut self, rhs: Int) {
            *self = self.div(rhs);
        }
    }
}
