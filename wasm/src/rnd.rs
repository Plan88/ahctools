use itertools::Itertools;
use rand::{seq::SliceRandom, Rng, RngCore};
use rand_chacha::{rand_core::SeedableRng, ChaCha20Rng};
use rand_distr::{Distribution, Normal};

use crate::generator;

pub struct RNG {
    rng: ChaCha20Rng,
}

impl RNG {
    pub fn new(seed: u64) -> Self {
        Self { rng: get_rng(seed) }
    }

    pub fn gen_normal(&mut self, mean: f64, std: f64) -> f64 {
        let normal_dist = Normal::<f64>::new(mean, std).unwrap();
        normal_dist.sample(&mut self.rng)
    }

    pub fn gen_range(&mut self, low: usize, high: usize, equal: bool) -> usize {
        if equal {
            self.rng.gen_range(low..=high)
        } else {
            self.rng.gen_range(low..high)
        }
    }

    pub fn gen_bool(&mut self, prob: f64) -> bool {
        self.rng.gen_bool(prob.clamp(0.0, 1.0))
    }

    pub fn gen_permutation(&mut self, n: usize) -> Vec<usize> {
        let mut permutation: Vec<usize> = (1..=n).collect();
        permutation.shuffle(&mut self.rng);
        permutation
    }
}

fn get_rng(seed: u64) -> ChaCha20Rng {
    ChaCha20Rng::seed_from_u64(seed)
}
