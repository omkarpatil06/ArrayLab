# Mathematical contract

## Coordinates and signs

Sensors lie along x with centred coordinates x_m in metres. The 2D source-bearing
unit vector is u(theta)=(sin(theta), cos(theta)). Broadside is theta=0 on +y;
positive bearings turn toward +x. The visible search sector is [-pi/2, pi/2].
This restriction does not remove the physical front/back ambiguity of a linear
array: bearings with equal x projection cannot be distinguished.

Use analytic pressure with time convention exp(+j 2 pi f t). A source at R u has
path length approximately R - x_m sin(theta). Relative arrival delay is therefore
 tau_m=-x_m sin(theta)/c. Removing the common carrier and reference delay gives

 a_m(theta)=exp(-j 2 pi f tau_m)=exp(+j 2 pi f x_m sin(theta)/c).

The wave propagates toward -u; source bearing and propagation direction must not
be interchanged. A positive-bearing source reaches sensors at larger x earlier.
All APIs take radians, Hz, metres and m/s. Frequency f is the carrier frequency,
not the envelope sampling rate. Sensor data X has shape (M,N); steering and weights
have shape (M,). Snapshots are complex envelopes, not real microphone samples.

## Assumptions

Homogeneous medium, identical omnidirectional calibrated sensors, static far-field
sources, no spreading differences, no reverberation, no mutual coupling. For
aperture D and envelope bandwidth B, require B D/c << 1 for phase-only narrowband
processing. The exact rank-one simulator assumes this approximation rather than
simulating propagation delays. Far field also requires negligible wavefront
curvature (commonly assessed relative to D^2/lambda and range).

The initial example uses a constant complex envelope (a pure carrier). There is
no sample-rate control because this simulator does not implement time-domain
propagation. Future physical waveforms will require a documented envelope sample
rate, bandwidth and delay model. An iid complex random envelope is useful for
statistical snapshots but should not be described as a physically bandlimited
waveform without further construction.

## Conventional beamforming

X=a(theta)s^T+V; for several sources sum each component separately.
Choose w=a(theta_0)/M. With unit-modulus steering, w^H a(theta_0)=1 and y=w^H X.
This is narrowband phase-shift delay-and-sum, not a fractional-delay time-domain
implementation. Spatial power gain is G(theta)=|w^H a(theta)|^2; do not divide
by the observed plot maximum, which could hide a normalization error.

For a ULA, psi=2 pi f d/c [sin(theta)-sin(theta_0)] and

 G(theta)=|sin(M psi/2)/(M sin(psi/2))|^2,

with the continuous limit G=1 at psi=2 pi k. Nulls occur at psi=2 pi q/M
unless the denominator also vanishes. Tests compare this closed form with the
implementation, and check an explicit two-sensor phase reference independently.

For independent sensor noise E[v v^H]=sigma^2 I, output noise power is
sigma^2 ||w||^2=sigma^2/M. At the correct look direction, desired power stays P_s,
so SNR_out=M P_s/sigma^2: gain 10 log10(M) dB. This is not a guaranteed SINR gain
in directional interference. SNR means desired/noise; SINR means
desired/(interference+noise). Preserve the separate components when evaluating.

Spacing d>lambda/2 permits grating lobes over the visible sector; equality has
an ambiguity between the two endfire endpoints. Larger spacing is intentionally
allowed for experiments. A ULA cannot uniquely estimate a full-circle bearing.
