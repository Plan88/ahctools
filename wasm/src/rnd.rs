use itertools::Itertools;
use rand::{seq::SliceRandom, SeedableRng};
use rand_chacha::ChaCha20Rng;
use rand_distr::{Distribution, Normal};

use crate::generator;

fn get_rng(seed: u64) -> ChaCha20Rng {
    ChaCha20Rng::seed_from_u64(seed)
}

fn get_normal(rng: &mut ChaCha20Rng, mean: f64, std: f64) -> f64 {
    let normal_dist = Normal::<f64>::new(mean, std).unwrap();
    normal_dist.sample(rng)
}

pub fn gen_permutation(seed: u64) -> String {
    let mut rng = get_rng(seed);
    let n = generator::get_n(seed as usize);
    let mut perm = (1..=n * n).collect_vec();
    perm.shuffle(&mut rng);

    let mut s = "".to_string();
    for (i, pi) in perm.into_iter().enumerate() {
        s += &pi.to_string();
        s += if i % n == n - 1 { "\n" } else { " " };
    }

    s
}
