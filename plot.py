import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import datetime as dt
import numpy as np
import seaborn as sns

def crashes(data, symbol, save=False):
    """Create an enhanced, more visually appealing chart of market crashes."""
    
    # Chart text and styling configuration
    strs = {
        '^BVSP': {
            'title': 'Ibovespa: Major Market Drawdowns Comparison',
            'subtitle': 'Historical perspective on current market conditions',
            'xlabel': 'Trading days since peak',
            'note': 'Data since 1996 • Updated: {}',
            'id': 'ibov'
        },
        '^GSPC': {
            'title': 'S&P 500 Historical Drawdowns',
            'subtitle': 'Comparing current sell-off with major historical crashes',
            'xlabel': 'Trading days since peak',
            'note': 'Data since 1927 • Updated: {}',
            'id': 'sp500'
        }
    }

    # Set up improved color palette
    current_color = '#E6550D'    # Bright orange for current crash
    worst_color = '#756bb1'      # Purple for worst crash
    notable_color = '#2ca02c'    # Green for notable crashes
    other_color = '#bdbdbd'      # Light gray for other crashes
    
    # Set up the plot with a modern style
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 8), dpi=100)
    fig.patch.set_facecolor('#f8f9fa')
    ax.set_facecolor('#f8f9fa')
    
    # Find all-time high and worst crash
    ath = data['value'].max()
    all_crashes = []
    
    # Collect data about each crash for better labeling
    for x in data['cummax'].unique():
        sub = data[data['cummax'] == x]
        if sub['delta'].min() < -.02:  # Only include actual drawdowns
            crash_year = str(sub['d'].values[0])[:4]
            min_value = sub['delta'].min()
            all_crashes.append((x, crash_year, min_value))
    
    # Sort crashes by severity
    all_crashes.sort(key=lambda x: x[2])
    
    # Identify current, worst, and notable crashes
    worst_crash = all_crashes[0][0] if all_crashes else None
    current_crash = ath
    
    # Find 2-3 notable historical crashes (not current, not worst)
    notable_crashes = []
    for x, year, value in all_crashes[1:7]:  # Take 2nd-7th worst crashes
        if x != current_crash and value < -0.25:  # Only if severe enough
            notable_crashes.append(x)
    
    # Plot all crashes with appropriate styling
    for x in data['cummax'].unique():
        sub = data[data['cummax'] == x]
        if sub['delta'].min() < -.02:
            # Determine appropriate styling for this crash
            if x == current_crash:
                color = current_color
                alpha = 1.0
                linewidth = 3.0
                zorder = 10
                marker_size = 80
            elif x == worst_crash:
                color = worst_color
                alpha = 0.9
                linewidth = 2.5
                zorder = 9
                marker_size = 60
            elif x in notable_crashes:
                color = notable_color
                alpha = 0.8
                linewidth = 2.0
                zorder = 8
                marker_size = 30
            else:
                color = other_color
                alpha = 0.4 + (sub['delta'].min() * -1) * 0.5  # Scale opacity by severity
                linewidth = 1.0
                zorder = 5
                marker_size = 20
            
            # Plot the crash line
            ax.plot(sub['ord_d'], sub['delta'], 
                   color=color, 
                   alpha=alpha, 
                   linewidth=linewidth,
                   zorder=zorder,
                   solid_capstyle='round')
            
            # Add end marker
            ax.scatter(sub['ord_d'].max(),
                      sub['delta'].values[-1],
                      color=color,
                      alpha=alpha,
                      s=marker_size,
                      zorder=zorder+1,
                      marker='o',
                      edgecolor='white')
            
            # Add labels for important crashes
            if (x == current_crash or 
                x == worst_crash or 
                x in notable_crashes or 
                sub['delta'].min() < -0.35):
                
                year = str(sub['d'].values[0])[:4]
                value = sub['delta'].values[-1]
                
                # Create nicer label
                if x == current_crash:
                    label = f"Current ({year}): {value:.1%}"
                else:
                    label = f"{year}: {value:.1%}"
                
                # Determine text position
                if year in ['2018', '2004', '1987', '2020', '2022']:
                    ha = 'left'
                    x_offset = 5
                else:
                    ha = 'right'
                    x_offset = -5
                
                # Add text label with slightly larger font
                ax.text(sub['ord_d'].max() + x_offset,
                       sub['delta'].values[-1],
                       label,
                       color=color,
                       fontsize=10,
                       fontweight='bold' if x == current_crash else 'normal',
                       ha=ha,
                       va='center',
                       bbox=dict(
                           boxstyle="round,pad=0.3", 
                           fc='white', 
                           ec=color if x == current_crash else 'none',
                           alpha=0.8
                       ))
    
    # Add horizontal lines for reference
    for level in [0, -0.1, -0.2, -0.3, -0.4, -0.5]:
        ax.axhline(
            y=level, 
            color='gray', 
            linestyle='--', 
            alpha=0.3, 
            zorder=1
        )
        # Label the lines
        if level != 0:
            ax.text(
                0, level, 
                f"{level:.0%}", 
                va='center', 
                ha='left',
                fontsize=9,
                color='gray',
                bbox=dict(fc='white', ec='none', alpha=0.8, pad=1)
            )
    
    # Improve chart styling
    
    # Set appropriate limits
    min_y = min(sub['delta'].min() for x in data['cummax'].unique() 
                if (sub := data[data['cummax'] == x])['delta'].min() < -0.02)
    ax.set_ylim(min(min_y * 1.1, -0.55), 0.05)  # Add some padding
    
    # Remove unnecessary spines
    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_visible(False)
    
    # Hide tick marks but keep labels
    ax.tick_params(axis='both', which='both', bottom=False, top=False, left=False, 
                  right=False, labelbottom=True, labeltop=False, labelleft=True, 
                  labelright=False, labelsize=10)
    
    # Improve grid (behind the data)
    ax.grid(axis='y', color='gray', linestyle='-', linewidth=0.5, alpha=0.3, zorder=0)
    
    # Use proper percentage formatter for y-axis
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    
    # Add titles and labels with improved typography
    fig.suptitle(strs[symbol]['title'], fontsize=24, fontweight='bold', 
                color='#333333', y=0.98)
    ax.set_title(strs[symbol]['subtitle'], fontsize=14, color='#666666', pad=10)
    ax.set_xlabel(strs[symbol]['xlabel'], fontsize=12)
    ax.set_ylabel('Drawdown from Peak', fontsize=12)
    
    # Add a footnote
    now = dt.datetime.today().strftime('%Y-%m-%d')
    note_text = strs[symbol]['note'].format(now)
    fig.text(0.02, 0.02, note_text, ha='left', va='bottom', 
             fontsize=9, color='#666666')
    
    # Add a legend to explain the color scheme
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color=current_color, lw=3, label='Current Drawdown'),
        Line2D([0], [0], color=worst_color, lw=2.5, label='Worst Historical'),
        Line2D([0], [0], color=notable_color, lw=2, label='Notable Historical'),
        Line2D([0], [0], color=other_color, lw=1, alpha=0.7, label='Other Drawdowns')
    ]
    ax.legend(handles=legend_elements, loc='upper right', frameon=True, 
             fontsize=10, facecolor='white', framealpha=0.9)
    
    plt.tight_layout(pad=1.5)
    
    # Save or display the figure
    if save:
        plt.savefig('img/crash_{}.png'.format(strs[symbol]['id']), 
                   dpi=150, bbox_inches='tight', facecolor='#f8f9fa')
        print(f"Enhanced crash chart saved to img/crash_{strs[symbol]['id']}.png")
    else:
        plt.show()


def drawdown(data, symbol):
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.plot(data['d'], data['drawdown'])
    
    # Improve grid styling
    ax.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    
    # Remove unnecessary spines
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Hide tick marks but keep labels
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True)
    plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=True)
    
    # Use ticker formatter for percentage
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    
    # Set title
    plt.title('{} Drawdown'.format(symbol))
    
    plt.show()


def recover(data, symbol, save=False):
    """Create an enhanced chart showing market recovery patterns after bottoms."""
    
    # Chart text and styling configuration
    strs = {
        '^BVSP': {
            'title': 'Ibovespa Recovery Patterns',
            'subtitle': 'Market behavior after reaching bottoms',
            'xlabel': 'Trading days since market bottom',
            'ylabel': 'Recovery from bottom (%)',
            'note': 'Data since 2000 • Updated: {}',
            'id': 'ibov'
        },
        '^GSPC': {
            'title': 'S&P 500 Recovery Patterns',
            'subtitle': 'How markets recover after significant drawdowns',
            'xlabel': 'Trading days since market bottom',
            'ylabel': 'Recovery from bottom (%)',
            'note': 'Data since 1927 • Updated: {}',
            'id': 'sp500'
        }
    }

    # Enhanced color palette
    current_color = '#1f77b4'   # Blue for current recovery
    fast_color = '#2ca02c'      # Green for fast recoveries
    slow_color = '#d62728'      # Red for slow recoveries
    other_color = '#7f7f7f'     # Gray for other recoveries
    
    # Set up the plot with a modern style
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 8), dpi=100)
    fig.patch.set_facecolor('#f8f9fa')
    ax.set_facecolor('#f8f9fa')
    
    # Find all-time high for identifying current period
    ath = data['value'].max()
    all_recoveries = []
    
    # Process data to identify different types of recoveries
    for x in data['cummax'].unique():
        if 'min' not in data.columns:
            continue
            
        sub = data[data['cummax'] == x]
        # Apply the same filtering as in the original
        sub_d = sub['ord_d'].max() if 'ord_d' in sub.columns else 0
        
        if 'ord_d' in sub.columns:
            sub = sub[sub['ord_d'] >= -100]
            sub = sub[sub['ord_d'] <= 100]
        
        if 'min' in sub.columns and sub['min'].min() < .98:
            # Track recovery metrics
            recovery_year = str(sub['d'].values[0])[:4]
            recovery_max = sub['cumdelta'].max() if 'cumdelta' in sub.columns else 0
            recovery_speed = recovery_max / (sub_d + 1) if sub_d > 0 else 0
            all_recoveries.append((x, recovery_year, recovery_max, recovery_speed))
    
    # Sort recoveries by speed
    if all_recoveries:
        all_recoveries.sort(key=lambda x: x[3], reverse=True)
        
        # Identify different recovery types
        current_recovery = ath
        fast_recoveries = [r[0] for r in all_recoveries[:3] if r[0] != current_recovery]
        slow_recoveries = [r[0] for r in all_recoveries[-3:] if r[0] != current_recovery]
    
        # Plot recoveries with appropriate styling
        for x in data['cummax'].unique():
            if 'min' not in data.columns:
                continue
                
            sub = data[data['cummax'] == x]
            if 'ord_d' in sub.columns:
                sub_d = sub['ord_d'].max()
                sub = sub[sub['ord_d'] >= -100]
                sub = sub[sub['ord_d'] <= 100]
            
            # Only proceed if we have the necessary columns and data meets criteria
            if 'min' in sub.columns and 'cumdelta' in sub.columns and sub['min'].min() < .98:
                # Determine styling
                if x == current_recovery:
                    color = current_color
                    alpha = 1.0
                    linewidth = 3.0
                    zorder = 10
                    marker_size = 80
                    label_size = 11
                    is_bold = True
                elif x in fast_recoveries:
                    color = fast_color
                    alpha = 0.8
                    linewidth = 2.0
                    zorder = 8
                    marker_size = 60
                    label_size = 10
                    is_bold = False
                elif x in slow_recoveries:
                    color = slow_color
                    alpha = 0.8
                    linewidth = 2.0
                    zorder = 8
                    marker_size = 60
                    label_size = 10
                    is_bold = False
                else:
                    color = other_color
                    alpha = 0.3 + (1 - sub['min'].min()) * 0.5  # Opacity based on drawdown magnitude
                    linewidth = 1.0
                    zorder = 5
                    marker_size = 40
                    label_size = 9
                    is_bold = False
                
                # Plot the recovery
                ax.plot(sub['ord_d'], sub['cumdelta'],
                       color=color,
                       alpha=alpha,
                       linewidth=linewidth,
                       zorder=zorder,
                       solid_capstyle='round')
                
                # Add end marker
                ax.scatter(sub['ord_d'].max(),
                          sub['cumdelta'].values[-1],
                          color=color,
                          alpha=alpha,
                          s=marker_size,
                          zorder=zorder+1,
                          marker='o',
                          edgecolor='white')
                
                # Add labels for notable recoveries
                if (x == current_recovery or 
                    x in fast_recoveries or 
                    x in slow_recoveries or 
                    sub['cumdelta'].max() > 0.5):  # Also label big recoveries
                    
                    year = str(sub['d'].values[0])[:4]
                    value = sub['cumdelta'].values[-1]
                    
                    # Determine label content
                    if x == current_recovery:
                        label = f"Current ({year}): +{value:.1%}"
                    else:
                        label = f"{year}: +{value:.1%}"
                    
                    # Determine label position
                    ha = 'left' if year in ['2018'] else 'right'
                    x_offset = 5 if ha == 'left' else -5
                    
                    # Add text label
                    ax.text(sub['ord_d'].max() + x_offset,
                           sub['cumdelta'].values[-1],
                           label,
                           color=color,
                           fontsize=label_size,
                           fontweight='bold' if is_bold else 'normal',
                           ha=ha,
                           va='center',
                           bbox=dict(
                               boxstyle="round,pad=0.3",
                               fc='white',
                               ec=color if x == current_recovery else 'none',
                               alpha=0.8
                           ))
    
    # Add horizontal reference lines
    for level in [0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        ax.axhline(
            y=level,
            color='gray',
            linestyle='--',
            alpha=0.3,
            zorder=1
        )
        # Label the lines
        ax.text(
            0, level,
            f"+{level:.0%}",
            va='center',
            ha='left',
            fontsize=9,
            color='gray',
            bbox=dict(fc='white', ec='none', alpha=0.8, pad=1)
        )
    
    # Add a vertical line at day 0 (the bottom)
    ax.axvline(x=0, color='gray', linestyle='-', alpha=0.5, zorder=2)
    ax.text(0, -0.05, "Bottom", ha='center', va='top', fontsize=10, 
           color='black', bbox=dict(fc='white', ec='gray', alpha=0.9, pad=2))
    
    # Improve chart styling
    
    # Set appropriate limits for x and y axes
    ax.set_xlim(-50, 100)
    ax.set_ylim(-0.05, 1.2)  # Allow some space for high recoveries
    
    # Remove unnecessary spines
    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_visible(False)
    
    # Hide tick marks but keep labels
    ax.tick_params(axis='both', which='both', bottom=False, top=False, left=False,
                  right=False, labelbottom=True, labeltop=False, labelleft=True,
                  labelright=False, labelsize=10)
    
    # Improve grid
    ax.grid(axis='both', color='gray', linestyle='-', linewidth=0.5, alpha=0.2)
    
    # Use proper percentage formatter for y-axis
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    
    # Add titles and labels with improved typography
    fig.suptitle(strs[symbol]['title'], fontsize=24, fontweight='bold',
                color='#333333', y=0.98)
    ax.set_title(strs[symbol]['subtitle'], fontsize=14, color='#666666', pad=10)
    ax.set_xlabel(strs[symbol]['xlabel'], fontsize=12)
    ax.set_ylabel(strs[symbol]['ylabel'], fontsize=12)
    
    # Add a footnote
    now = dt.datetime.today().strftime('%Y-%m-%d')
    note_text = strs[symbol]['note'].format(now)
    fig.text(0.02, 0.02, note_text, ha='left', va='bottom',
             fontsize=9, color='#666666')
    
    # Add a legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color=current_color, lw=3, label='Current Recovery'),
        Line2D([0], [0], color=fast_color, lw=2, label='Fast Recoveries'),
        Line2D([0], [0], color=slow_color, lw=2, label='Slow Recoveries'),
        Line2D([0], [0], color=other_color, lw=1, alpha=0.7, label='Other Periods')
    ]
    ax.legend(handles=legend_elements, loc='upper right', frameon=True,
             fontsize=10, facecolor='white', framealpha=0.9)
    
    plt.tight_layout(pad=1.5)
    
    # Save or display the figure
    if save:
        plt.savefig('img/recovery_{}.png'.format(strs[symbol]['id']),
                   dpi=150, bbox_inches='tight', facecolor='#f8f9fa')
        print(f"Enhanced recovery chart saved to img/recovery_{strs[symbol]['id']}.png")
    else:
        plt.show()


def crash_2020_trajectories(data):
    fall_values = data.groupby('symbol').last().reset_index()
    fall_values = fall_values.sort_values('cumdelta')
    n = min(16, int(fall_values.shape[0]/2))
    top_symbols = fall_values['symbol'].values[:n]
    bottom_symbols = fall_values['symbol'].values[-n:]
    
    # Create a color palette
    colors = sns.color_palette("RdBu", n_colors=fall_values.shape[0]).as_hex()

    top_domain = np.mean(fall_values['cumdelta'].values[:n]) + np.array([.06, -.06])
    top_range = list(np.linspace(top_domain[0], top_domain[1], n))

    bottom_domain = np.mean(fall_values['cumdelta'].values[-n:]) + np.array([.06, -.06])
    bottom_range = list(np.linspace(bottom_domain[0], bottom_domain[1], n))

    fig, ax = plt.subplots(figsize=(10, 5))
    
    for symbol in fall_values['symbol']:
        equity_data = data[data['symbol'] == symbol]
        color = colors.pop(0)
        alpha = .66 if symbol in top_symbols or symbol in bottom_symbols else .2
        plt.plot(equity_data['d'],
                 equity_data['cumdelta'],
                 c=color,
                 linewidth=1.0,
                 alpha=alpha)

        if symbol in top_symbols:
            plt.text(equity_data['d'].values[-1],
                     top_range.pop(),
                     '{} {:.1%}'.format(symbol, equity_data['cumdelta'].values[-1]),
                     c=color)
        if symbol in bottom_symbols:
            plt.text(equity_data['d'].values[-1],
                     bottom_range.pop(),
                     '{} {:.1%}'.format(symbol, equity_data['cumdelta'].values[-1]),
                     c=color)

    # Improve grid styling
    ax.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    
    # Remove unnecessary spines
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Hide tick marks but keep labels
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True)
    plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=True)
    
    # Set title
    plt.title('Quedas do crash de 2020')
    
    # Use ticker formatter for percentage
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

    plt.show()
